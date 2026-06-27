# Rust 面试八股文

> 候选人：周景潇 | 2026-06-27 | 主力语言：Rust | 3 个大型开源项目（44+ crate, 2000+ 测试）
> 求职方向：AI Agent 开发 / 后端开发 / 系统开发
> 项目特征：tokio/axum/egui/ratatui，parking_lot 生产使用，零 unwrap 策略，Candle FFI

---

## 1. 所有权与借用（必考）

### 1.1 三条所有权规则

1. Rust 中每个值有且仅有一个**所有者（owner）**
2. 同一时刻只能有一个所有者
3. 所有者离开作用域时，值被 drop（Drop trait 调用）

### 1.2 内存管理模型对比

| 维度 | GC（Java/Go） | 手动（C/C++） | 所有权（Rust） |
|------|-------------|-------------|--------------|
| 分配 | 运行时堆分配 | 显式 malloc/new | 编译期栈/Box 决策 |
| 释放 | GC 周期扫描 | 显式 free/delete | 编译器插入 drop（作用域结束） |
| 运行时开销 | STW/并发标记 | 近乎零 | **零开销**（编译期静态分析） |
| 内存安全 | 无 use-after-free | 悬垂指针/双重释放 | 借用检查器编译期消除 |
| 数据竞争 | 运行时检测 | 纯约定无保护 | 编译期消除（Send/Sync） |
| 确定性析构 | 否（finalizer不可靠） | 是但手动 | **是**（Drop trait, RAII） |

**面试金句**：Rust 的所有权系统本质上是**编译期 GC**——借用检查器在编译时完成静态分析，消除 GC 运行时开销，同时达到 C++ 级别的性能。

### 1.3 引用与借用规则

- **不可变引用 `&T`**：可以有多个，只读，与可变引用互斥
- **可变引用 `&mut T`**：同一时刻只有一个，独占读写
- **NLL**：Rust 2018 起引用作用域从词法作用域变为最后一次使用位置
- **reborrow**：可变引用可以临时再借用为不可变引用

```rust
let mut v = vec![1, 2, 3];
let r1 = &v; let r2 = &v;     // 多个不可变引用 OK
println!("{} {}", r1, r2);     // r1, r2 最后使用
let r3 = &mut v;               // OK: NLL，r1/r2 已不再使用
r3.push(4);
```

### 1.4 生命周期标注

**生命周期省略规则（三条）**：
1. 每个引用参数获得独立的生命周期参数
2. 如果只有一个输入生命周期参数，它被赋给所有输出生命周期参数
3. 如果有多个输入生命周期参数，但其中一个是 `&self` 或 `&mut self`，则 `self` 的生命周期赋给所有输出

```rust
// 规则1：fn foo<'a>(x: &'a str)
fn foo(x: &str) -> &str { x }

// 规则3：self 的生命周期赋给输出
impl<'a> MyStruct<'a> {
    fn get(&self, key: &str) -> &str { ... }  // 输出有 self 的生命周期
}
```

**结构体中的生命周期**：
```rust
struct Excerpt<'a> {
    content: &'a str,  // Excerpt 不能比 content 活得更久
}
```

**闭包中的生命周期**：
```rust
// 闭包捕获引用的生命周期受限于闭包的调用时机
let mut v = vec![1, 2, 3];
let mut closure = || v.push(4);  // 捕获 &mut v
closure();  // 必须在 v 被其他借用之前调用
```

---

## 2. 智能指针与内存管理

### 2.1 Box<T>

```rust
// 堆分配，独占所有权，大小已知（指针大小）
let b: Box<i32> = Box::new(5);

// 使用场景：
// 1. 递归类型（大小无法在编译时确定）
enum List { Cons(i32, Box<List>), Nil }

// 2. 大对象从栈移到堆
let big_array = Box::new([0u8; 10_000_000]);

// 3. trait object（dyn Trait 的大小未知）
let handler: Box<dyn Fn()> = Box::new(|| println!("hi"));
```

### 2.2 Rc<T> vs Arc<T>

| 特性 | Rc<T> | Arc<T> |
|------|-------|--------|
| 引用计数 | 非原子操作 | 原子操作（AtomicUsize） |
| 线程安全 | 否（!Send, !Sync） | 是（Send + Sync） |
| 性能 | 快 | 稍慢（原子操作开销） |
| 使用场景 | 单线程共享所有权 | 多线程共享所有权 |

```rust
// Rc 示例：单线程共享
use std::rc::Rc;
let a = Rc::new(vec![1, 2, 3]);
let b = Rc::clone(&a);  // ref count = 2
let c = Rc::clone(&a);  // ref count = 3

// Arc 示例：多线程共享
use std::sync::Arc;
let a = Arc::new(vec![1, 2, 3]);
let b = Arc::clone(&a);
std::thread::spawn(move || {
    println!("{:?}", b);  // Arc 是 Send，可以移到其他线程
});
```

### 2.3 RefCell<T> 和内部可变性

```rust
use std::cell::RefCell;

// 运行时借用检查（而非编译时）
let data = RefCell::new(vec![1, 2, 3]);
{
    let mut v = data.borrow_mut();  // 可变借用
    v.push(4);
}  // v 离开作用域，释放借用
let v = data.borrow();  // 不可变借用 OK
println!("{:?}", v);
```

**Cell<T> vs RefCell<T>**：Cell 使用 Copy/Replace 语义（适用 Copy 类型），RefCell 使用引用语义（适用非 Copy 类型）。

### 2.4 parking_lot vs std::sync

候选人项目中使用 parking_lot 而非 std::sync：

| 特性 | std::sync::Mutex | parking_lot::Mutex |
|------|-----------------|-------------------|
| 实现 | 操作系统互斥锁 | 用户态自旋+操作系统fallback |
| 中毒 | 有中毒机制（panic时poison） | 无中毒（panic时直接解锁） |
| 性能 | 较慢 | 更快（减少系统调用） |
| 公平性 | 依赖OS调度 | 公平锁 |
| 功能 | 基础 | 支持 try_lock, lock_arc 等 |

```rust
// parking_lot 生产使用
use parking_lot::Mutex;
let lock = Mutex::new(0);
{
    let mut guard = lock.lock();   // 无 Result，不会中毒
    *guard += 1;
}  // guard 离开作用域自动解锁
```

**面试必答**：选择 parking_lot 的三个原因 —— 1) 性能更好（减少系统调用），2) 无中毒机制更符合实际使用（panic 不应传播到其他线程的锁等待），3) 更丰富的 API（try_lock_for, lock_arc 等）。

---

## 3. Trait 与泛型（必考）

### 3.1 静态分发 vs 动态分发

```rust
// 静态分发（单态化）：编译时为每个具体类型生成代码
fn process<T: Display>(item: T) { println!("{}", item); }
// 编译后生成：process::<i32>, process::<String>, process::<f64> ...

// 动态分发（vtable）：运行时通过函数指针调用
fn process_dyn(item: &dyn Display) { println!("{}", item); }
```

| 维度 | 静态分发 | 动态分发 |
|------|---------|---------|
| 机制 | 单态化（编译时） | vtable（运行时） |
| 性能 | 更快（无间接调用开销，可内联） | 稍慢（指针间接调用） |
| 二进制大小 | 更大（每种类型生成一份代码） | 更小（一份代码） |
| 灵活性 | 编译时确定，不能异构集合 | 运行时多态，可放入 Vec<Box<dyn Trait>> |

### 3.2 Trait Object 安全规则

trait 可以转换为 trait object（`dyn Trait`）当且仅当：
1. 所有方法中不包含泛型参数（非 `Self` 的泛型可以）
2. 所有方法的接收者必须是 `self`、`&self`、`&mut self`、`Box<self>` 等
3. 不包含返回 `Self` 的方法（除接收者外）
4. 不包含关联常量

```rust
// Object-safe: OK
trait Drawable { fn draw(&self); }
let v: Vec<Box<dyn Drawable>> = vec![];  // OK

// Not object-safe: 有泛型方法
trait Parser {
    fn parse<T: FromStr>(&self, input: &str) -> Result<T, T::Err>;
}
// let v: Vec<Box<dyn Parser>> = vec![];  // 编译错误
```

### 3.3 关联类型 vs 泛型参数

```rust
// 关联类型：每个实现可以选择一个具体类型
trait Iterator {
    type Item;  // 关联类型
    fn next(&mut self) -> Option<Self::Item>;
}

// 泛型参数：调用方指定类型
trait Converter<T> {
    fn convert(&self, input: T) -> String;
}
```

**选择标准**：
- 如果每个 impl 块应该只关联一个具体类型 → 用关联类型（如 Iterator 的 Item）
- 如果同一个类型可以有多个实现（如 From<i32>, From<String>）→ 用泛型参数

### 3.4 标准库关键 Trait

| Trait | 用途 | 自动实现 |
|-------|------|---------|
| `Display` | 用户友好的格式化 | 否 |
| `Debug` | 调试输出 | 可 derive |
| `Clone` | 显式复制 | 可 derive |
| `Copy` | 隐式复制（位拷贝） | 可 derive（但需所有字段是 Copy） |
| `PartialEq / Eq` | 相等比较 | 可 derive |
| `PartialOrd / Ord` | 排序 | 可 derive |
| `Hash` | 哈希 | 可 derive |
| `Default` | 默认值 | 可 derive |
| `From / Into` | 类型转换 | `From<T> for U` 自动提供 `Into<U> for T` |
| `Send` | 可安全转移到其他线程 | 编译器自动推导 |
| `Sync` | 可安全跨线程共享引用 | 编译器自动推导 |
| `Deref` | 解引用 `*t` | 手动实现 |
| `Drop` | 析构 | 手动实现 |

### 3.5 Send 和 Sync 的自动推导

```rust
// Send: T 可以安全地将所有权转移到另一个线程
// 如果 T 的所有字段都是 Send，则 T 自动是 Send

// Sync: &T 可以安全地被多个线程同时访问
// 如果 T 的所有字段都是 Sync，则 T 自动是 Sync

// 特例：
// Rc<T> 既不是 Send 也不是 Sync（非原子引用计数）
// RefCell<T> 是 Send（如果 T 是 Send）但不是 Sync（运行时借用检查非线程安全）
// Mutex<T> 是 Send + Sync（如果 T 是 Send）
// Arc<T> 是 Send + Sync（如果 T 是 Send + Sync）
```

---

## 4. 错误处理

### 4.1 Result<T, E> vs panic!

Rust 的错误处理哲学：
- **可恢复错误** → `Result<T, E>`
- **不可恢复错误** → `panic!`（仅用于 bug、不变量违反、测试）

候选人项目的**零 unwrap 策略**：
```rust
// 被 CI 拒绝
let config = std::fs::read_to_string("config.toml").unwrap();

// CI 通过
let config = std::fs::read_to_string("config.toml")
    .map_err(|e| anyhow!("Failed to read config: {}", e))?;
```

### 4.2 ? 运算符

```rust
fn read_config() -> Result<Config, Box<dyn Error>> {
    let content = std::fs::read_to_string("config.toml")?;  // 自动错误转换
    let config: Config = toml::from_str(&content)?;         // From trait 自动转换
    Ok(config)
}
```

`?` 运算符 = 展开 Result：如果是 Err 则提前返回，如果是 Ok 则解包。同时通过 `From` trait 自动转换错误类型。

### 4.3 thiserror（库）vs anyhow（应用）

```rust
// thiserror: 用于库，定义精确的错误类型
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyLibError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("Parse error at line {line}: {msg}")]
    Parse { line: usize, msg: String },
    
    #[error("Not found: {0}")]
    NotFound(String),
}

// anyhow: 用于应用，简化错误传播
use anyhow::{Result, Context};
fn main() -> Result<()> {
    let content = std::fs::read_to_string("config.toml")
        .context("Failed to read config file")?;
    Ok(())
}
```

---

## 5. 并发与异步（必考）

### 5.1 Send 和 Sync 精确含义

- **Send**：类型 T 的所有权可以安全地从线程 A 转移到线程 B
- **Sync**：类型 T 的不可变引用 `&T` 可以安全地被多个线程同时访问
- 自动推导规则：如果 T 的所有字段都是 Send/Sync，则 T 自动是 Send/Sync

```rust
fn is_send<T: Send>() {}
fn is_sync<T: Sync>() {}

is_send::<i32>();       // ✓ i32 是 Send
is_send::<String>();    // ✓ String 是 Send
is_send::<Rc<i32>>();   // ✗ Rc 不是 Send（非原子引用计数）
is_sync::<Mutex<i32>>();// ✓ Mutex<i32> 是 Sync
is_sync::<RefCell<i32>>();// ✗ RefCell 不是 Sync（运行时借用检查非线程安全）
```

### 5.2 std::thread::spawn vs tokio::task::spawn

```rust
// std::thread: 适合 CPU 密集型任务
std::thread::spawn(|| {
    heavy_computation();
});

// tokio::task: 适合 I/O 密集型任务
tokio::task::spawn(async {
    let data = reqwest::get("https://api.example.com").await?;
    process(data).await
});

// tokio::task::spawn_blocking: 在 tokio 中运行 CPU 密集型任务
tokio::task::spawn_blocking(|| {
    heavy_computation();  // 不阻塞 async 线程池
}).await;
```

### 5.3 tokio::sync::Mutex vs std::sync::Mutex

```rust
// std::sync::Mutex: 适合同步代码或锁持有时间极短
use std::sync::Mutex;
let counter = Arc::new(Mutex::new(0));

// tokio::sync::Mutex: 适合异步代码中需要跨越 .await 持有锁
use tokio::sync::Mutex;
let cache = Arc::new(Mutex::new(HashMap::new()));

async fn get_or_fetch(cache: &Mutex<HashMap<String, Data>>, key: &str) -> Data {
    let mut guard = cache.lock().await;
    if let Some(data) = guard.get(key) {
        return data.clone();
    }
    drop(guard);  // 在 .await 前释放锁
    let data = fetch_from_network(key).await;
    let mut guard = cache.lock().await;
    guard.insert(key.to_string(), data.clone());
    data
}
```

**面试要点**：tokio::sync::Mutex 在锁竞争不激烈时与 std::sync::Mutex 性能相近，但 std::sync::Mutex 不能在 .await 点持有（Send 约束），而 tokio::sync::Mutex 可以。

### 5.4 Channel 全家桶

| Channel | 接收者数量 | 发送者数量 | 特点 | 使用场景 |
|---------|----------|----------|------|---------|
| `mpsc` | 单个 | 多个 | 多生产者单消费者 | 任务结果收集 |
| `broadcast` | 多个 | 单个 | 每个接收者收到所有消息 | 事件广播 |
| `watch` | 多个 | 单个 | 只保留最新值，新接收者看到最新值 | 配置变更通知 |
| `oneshot` | 单个 | 单个 | 一次性通信 | 请求-响应模式 |

```rust
// oneshot: 请求-响应
let (tx, rx) = tokio::sync::oneshot::channel();
tokio::spawn(async move {
    let result = compute().await;
    let _ = tx.send(result);  // 发送结果
});
let result = rx.await.unwrap();

// broadcast: 事件广播
let (tx, _) = tokio::sync::broadcast::channel(16);
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();
tx.send("event".to_string()).unwrap();
assert_eq!(rx1.recv().await.unwrap(), "event");
assert_eq!(rx2.recv().await.unwrap(), "event");
```

### 5.5 Future trait 和 Pin

```rust
// Future trait 的精简定义
pub trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

// Pin 的必要性：自引用结构
// async fn 生成的状态机可能包含指向自身的指针
// Pin 保证这种自引用结构不会被移动
```

### 5.6 死锁常见模式

```rust
// 模式1：锁顺序不一致
// 线程A：先锁 lock1 再锁 lock2
// 线程B：先锁 lock2 再锁 lock1  → 死锁

// 模式2：在持有锁时调用 .await（tokio）
let mut guard = cache.lock().await;
let data = fetch_network().await;  // .await 点可能让出控制权
// 其他任务可能也在等待同一个锁 → 死锁（或长时间阻塞）

// 模式3：Mutex 的 lock() 在持有 read lock 时再 lock
// RwLock: read lock → write lock = 死锁
```

---

## 6. unsafe Rust

### 6.1 unsafe 的 5 种能力

```rust
unsafe {
    // 1. 解引用原始指针
    let p: *const i32 = &42;
    let val = *p;
    
    // 2. 调用 unsafe 函数
    unsafe_fn();
    
    // 3. 访问可变静态变量
    static mut COUNTER: u32 = 0;
    COUNTER += 1;
    
    // 4. 实现 unsafe trait
    unsafe impl Send for MyType {}
    
    // 5. 访问 union 字段
    union MyUnion { i: i32, f: f32 }
    let u = MyUnion { i: 42 };
    let val = u.i;
}
```

### 6.2 使用 unsafe 的指导原则

候选人项目中的实践：
```rust
// SAFETY: ptr was validated non-null and properly aligned on line 42.
// The lifetime 'a is guaranteed by the caller to outlive this read.
unsafe { ptr.read() }

// SAFETY: This FFI call to Candle C API is safe because:
// 1. All tensor dimensions match the expected layout
// 2. Memory is owned by the Candle runtime, not Rust
// 3. The callback is 'static (no dangling references)
unsafe { candle_forward(ctx, tensor) }
```

**任何时候使用 unsafe 必须有 `// SAFETY:` 注释解释为什么是安全的。**

---

## 7. Cargo 与工程实践

### 7.1 Workspace 管理

```toml
[workspace]
members = ["crates/*", "cmd/*"]
resolver = "2"

[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

### 7.2 Feature Flags

```toml
[features]
default = ["tui", "mcp"]
tui = ["ratatui", "crossterm"]
mcp = ["serde_json"]
local-llm = ["candle-core", "tokenizers"]
```

### 7.3 发布配置

```toml
[profile.release]
lto = true               # 链接时优化
codegen-units = 1        # 单代码生成单元（更好的优化）
opt-level = 3            # 最大优化等级
strip = true             # 去除调试符号
```

---

## 8. 常见面试代码题

### 8.1 实现简化版 Arc

```rust
use std::sync::atomic::{AtomicUsize, Ordering};
use std::ops::Deref;

struct MyArc<T> {
    ptr: *const Inner<T>,
}

struct Inner<T> {
    data: T,
    ref_count: AtomicUsize,
}

impl<T> MyArc<T> {
    fn new(data: T) -> Self {
        let inner = Box::new(Inner {
            data,
            ref_count: AtomicUsize::new(1),
        });
        MyArc { ptr: Box::into_raw(inner) }
    }
}

impl<T> Clone for MyArc<T> {
    fn clone(&self) -> Self {
        unsafe {
            (*self.ptr).ref_count.fetch_add(1, Ordering::Relaxed);
        }
        MyArc { ptr: self.ptr }
    }
}

impl<T> Drop for MyArc<T> {
    fn drop(&mut self) {
        unsafe {
            if (*self.ptr).ref_count.fetch_sub(1, Ordering::Release) == 1 {
                std::sync::atomic::fence(Ordering::Acquire);
                drop(Box::from_raw(self.ptr as *mut Inner<T>));
            }
        }
    }
}

impl<T> Deref for MyArc<T> {
    type Target = T;
    fn deref(&self) -> &T {
        unsafe { &(*self.ptr).data }
    }
}
```

**面试要点**：必须解释 Acquire/Release 内存顺序的用途 —— Release 保证之前的写入对其他线程可见，Acquire 保证看到 Release 之前的所有写入。

### 8.2 实现线程池

```rust
use std::sync::{Arc, Mutex, mpsc};
use std::thread;

type Job = Box<dyn FnOnce() + Send + 'static>;

struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}

impl ThreadPool {
    fn new(size: usize) -> Self {
        let (tx, rx) = mpsc::channel::<Job>();
        let rx = Arc::new(Mutex::new(rx));
        let mut workers = Vec::with_capacity(size);
        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&rx)));
        }
        ThreadPool { workers, sender: Some(tx) }
    }

    fn execute<F>(&self, f: F)
    where F: FnOnce() + Send + 'static
    {
        self.sender.as_ref().unwrap().send(Box::new(f)).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());  // 关闭 channel
        for worker in &mut self.workers {
            if let Some(thread) = worker.thread.take() {
                thread.join().unwrap();
            }
        }
    }
}
```

---

## 9. Rust 2024 Edition 关键变化

候选人的项目使用 Rust 2024 edition：

- `impl Trait` 在返回位置的新语法
- 改进的 `unsafe` 块规则
- `gen` 块（实验性：async generators）
- 改进的模式匹配
- `!` 类型稳定化（Never type）

---

## 10. 面试策略

### 回答框架
- **直接回答** → 先给出结论
- **递进深入** → 从简单到复杂逐步展开
- **对比分析** → 与其他方案对比（Rust vs C++/Go/Java）
- **实战经验** → 结合候选人项目中的实际应用

### 必答题准备
1. 所有权和借用 → 准备 2-3 个实际代码示例
2. Send/Sync → 能解释为什么 Rc 不是 Send、RefCell 不是 Sync
3. async/await 原理 → 能解释 Future 状态机 + Pin
4. 错误处理 → 能说明 thiserror vs anyhow 的选择

### 加分项准备
5. 能解释为什么项目选 parking_lot 而非 std::sync
6. 能解释零 unwrap 策略的工程价值
7. 能展示 Cargo workspace 管理 22+ crate 的经验
8. 能讨论 unsafe 的使用边界和 SAFETY 注释规范

---

## 11. 面试常见追问与高质量回答

### Q: Rust 的所有权和 C++ RAII 的本质区别？

C++ RAII 是**约定**——程序员保证构造/析构配对，编译器不强制。Rust 所有权是**编译期验证的 RAII**——编译器跟踪每个值的所有者，确保 drop 在唯一所有者离开作用域时被调用，借用规则保证无悬垂引用。

### Q: Box<T> 和 C++ unique_ptr 的区别？

- `unique_ptr` 可为 null，`Box<T>` 不能为空（永远是有效堆分配）
- `unique_ptr` 支持自定义 deleter，`Box<T>` 只调用 `Drop::drop`
- `Box<dyn Trait>` 使用胖指针（ptr+vtable），`unique_ptr<Base>` 依赖虚函数表

### Q: 为什么不所有类型都实现 Copy？

如果都实现 Copy，将失去所有权系统的核心价值——确定性析构和移动语义。`String` 不实现 Copy 因为：1) 堆内存需唯一所有者释放；2) 隐式复制大对象有性能隐患；3) 资源（文件句柄/锁/socket）复制语义无意义。

### Q: tokio::spawn 和 std::thread::spawn 的资源消耗对比？

tokio task 是用户态协程——创建约几微秒，栈约几KB，上下文切换是用户态操作。std thread 是 OS 线程——创建约几毫秒，默认栈 8MB（Linux），上下文切换涉及内核态。一个 tokio 进程可管理数十万 task，OS 线程通常上限几千。代价是 tokio task 不能做 CPU 密集计算（阻塞调度器），需 `spawn_blocking` 分流。

---

## 12. 候选人项目中的 Rust 技术深度展示清单

| 技术点 | 项目 | 面试展示方式 |
|--------|------|-------------|
| 22 crate Contract-First 分层 | Clarity | 画依赖 DAG，解释 contract 为何零内部依赖 |
| SPMC 事件总线替代 RPC | Clarity | 对比 MPSC/SPMC/Broadcast 语义差异 |
| parking_lot over std::sync | Clarity | 基准对比 + 中毒机制取舍分析 |
| Candle GGUF FFI 边界 | Clarity | 展示 SAFETY 注释，解释谁负责释放 C 端内存 |
| 自定义 cosine_similarity SQL UDF | Devbase | 从 &[u8] 到 &[f32] 的零拷贝重解释 |
| 零 unwrap CI 强制策略 | Devbase | 展示 clippy.toml deny 规则 + CI 日志 |
| prost + rustls + ed25519 | Syncthing-rust | 展示 wire_compat 测试与 Go 版本对比 |
| sled COW B+Tree 选型 | Syncthing-rust | 对比 sled vs SQLite vs RocksDB 的适用场景 |
| rayon 并行 SHA-256 | Syncthing-rust | 对比单线程 vs rayon vs tokio 的性能差异 |

---

## 13. Rust 面试代码速查卡片

```rust
// HashMap entry API —— 一次查找完成插入或更新
map.entry(key).and_modify(|v| *v += 1).or_insert(1);

// VecDeque 双端队列 —— BFS/滑动窗口
let mut q = VecDeque::new();
q.push_back(root);
while let Some(node) = q.pop_front() { }

// BinaryHeap 优先队列 —— TopK（最大堆）
let mut heap = BinaryHeap::new();
heap.push(item);
let top = heap.pop().unwrap();

// Reverse 包装器 —— 最小堆
use std::cmp::Reverse;
let mut min_heap = BinaryHeap::new();
min_heap.push(Reverse(item));

// 迭代器链 —— 函数式数据处理
let result: Vec<i32> = nums.iter()
    .filter(|&&x| x > 0).map(|&x| x * 2)
    .take(5).collect();

// 模式匹配 —— 枚举/Option/Result 安全解构
match result {
    Ok(Some(value)) if value > 0 => handle(value),
    Ok(None) => handle_empty(),
    Err(e) => handle_error(e),
}

// ? 运算符链 —— 错误传播
fn process() -> Result<Output> {
    let input = read_file("input.txt")?;
    let parsed = parse(&input)?;
    Ok(transform(parsed)?)
}

// Arc+Mutex —— 多线程共享可变状态
let shared = Arc::new(Mutex::new(Vec::new()));
for i in 0..4 {
    let shared = Arc::clone(&shared);
    std::thread::spawn(move || {
        shared.lock().unwrap().push(i);
    });
}
```
