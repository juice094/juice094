#!/usr/bin/env python3
"""Generate the complete rust interview document."""

OUTPUT = r"C:\Users\22414\dev\juice094\求职战备\通用八股\rust-八股文.md"


def main():
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(part1())
        f.write(part2())
        f.write(part3())
        f.write(part4())
        f.write(part5())
        f.write(part6())
        f.write(part7())
        f.write(part8())
        f.write(part9())
        f.write(part10())
    with open(OUTPUT, "r", encoding="utf-8") as f:
        chars = len(f.read())
    print(f"Done: {chars} characters written to {OUTPUT}")


def part1():
    return r"""# Rust 面试八股文 通用技术面试备考手册

> 候选人：周景潇 | 2026-06-27
> 主力语言：Rust | 3 个大型开源项目（44+ crate, 2000+ 测试）
> 求职方向：AI Agent 开发 / 后端开发 / 系统开发
> 项目特征：tokio/axum/egui/ratatui 精通，parking_lot 生产使用，零 unwrap 策略，Candle FFI

---

## 目录

1. [所有权与借用](#1-所有权与借用)
2. [智能指针与内存管理](#2-智能指针与内存管理)
3. [Trait 与泛型](#3-trait-与泛型)
4. [错误处理](#4-错误处理)
5. [并发与异步](#5-并发与异步)
6. [unsafe Rust](#6-unsafe-rust)
7. [Cargo 与工程实践](#7-cargo-与工程实践)
8. [常见面试代码题](#8-常见面试代码题)
9. [Rust 2024 Edition 关键变化](#9-rust-2024-edition-关键变化)
10. [参考资源](#10-参考资源)

---

## 1. 所有权与借用

考察频率：必考 | 难度：中高 | 推荐回答方式：递进深入

### 1.1 所有权三条规则

**核心规则**（必须脱口而出）：

1. Rust 中每一个值都有一个被称为其**所有者**（owner）的变量。
2. 值在任一时刻**有且只有一个**所有者。
3. 当所有者离开作用域时，值将被**丢弃**（调用 `drop`）。

### 1.2 三种内存管理模型对比

| 维度 | GC（Java / Go） | 手动管理（C / C++） | 所有权（Rust） |
|------|-----------------|---------------------|---------------|
| 分配 | 运行时在堆上分配 | 显式 malloc/new | 编译期决定栈/堆（Box） |
| 释放时机 | GC 线程周期性扫描 | 显式 free/delete | 编译器在作用域末尾插入 drop |
| 运行时开销 | STW / 并发标记 | 几乎为零 | 零开销（编译期静态分析） |
| 内存安全 | 无 use-after-free | 悬垂指针、双重释放、泄漏 | 借用检查器在编译期杜绝 |
| 数据竞争 | 运行时检测或 lock | 无保护，纯靠约定 | 编译期杜绝（Send/Sync） |
| 确定性析构 | 无（finalizer 不可靠） | 有但靠人 | 有（Drop trait，RAII） |
| 循环引用 | GC 自动回收 | 手动打破 | 需 Weak 辅助或 Arena 批量释放 |

**面试金句**：

> Rust 的所有权系统本质上是一种**编译期的 GC**：借用检查器在编译时完成静态分析，将 GC 的运行时开销消除，同时获得了 C++ 级别的性能。

**对候选人项目的关联**：
- 44+ crate 的大型项目中，所有权系统保证了跨 crate 边界的资源安全，无需运行时开销。
- 在 Candle FFI 接口处，所有权规则清晰定义了谁负责释放 C 端分配的内存。

### 1.3 引用与借用

**不可变引用 `&T`**：可以存在多个，只读访问，和可变引用互斥。

**可变引用 `&mut T`**：同一时刻只能存在一个，独占读写权限。

**NLL（Non-Lexical Lifetimes）**：Rust 2018 Edition 引入，引用的作用域从"词法作用域"变为"最后一次使用的范围"。

```rust
fn nll_demo() {
    let mut data = vec![1, 2, 3];

    let r1 = &data;           // borrow starts
    let r2 = &data;           // borrow starts
    println!("{:?} {:?}", r1, r2); // last use of r1, r2
    // r1, r2 borrows end here (NLL), NOT at end of block

    let r3 = &mut data;       // OK: r1/r2 already ended
    r3.push(4);
}
```

在 Rust 2015（NLL 之前），上述代码编译失败——因为 r1 和 r2 的词法作用域延伸到 `r3` 声明位置。

**重借用（Reborrow）**：

```rust
fn reborrow_demo(mut v: Vec<i32>) {
    let r = &mut v;
    r.push(1);
    // r 最后一次使用

    let r2 = &mut *r;  // reborrow: 从 r 借用一个新的 &mut
    r2.push(2);
    // r2 作用域结束，r 重新可用
    r.push(3);  // OK
}
```

### 1.4 生命周期标注语法

**核心理解**：生命周期标注**不改变引用的实际生命周期**，它只是告诉编译器多个引用之间的约束关系。

#### 函数签名中的生命周期

```rust
// 输入和输出具有相同生命周期
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// 输出生命周期仅与一个输入相关
fn first<'a>(x: &'a str, _y: &str) -> &'a str {
    x
}

// 多个生命周期参数
fn split_at<'a, 'b>(s: &'a str, delimiter: &'b str) -> Option<&'a str> {
    s.find(delimiter).map(|pos| &s[..pos])
}
```

#### 结构体中的生命周期

```rust
// 结构体持有引用，必须标注生命周期
struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    // 省略规则 1 适用：&self 获得 'a
    fn announce_and_return(&self, announcement: &str) -> &str {
        println!("{}", announcement);
        self.part
    }
}
```

#### 闭包中的生命周期

```rust
// 闭包捕获引用时，生命周期由编译器自动推导
fn closure_lifetime() {
    let s = String::from("hello");
    let f = || println!("{}", s);  // 闭包不可变借用 s
    f();
    // f 最后一次调用，借用结束
    let s2 = s;  // OK: f 的借用已结束
}
```

### 1.5 生命周期省略规则（三条规则）

面试时必须准确说出三条规则：

**规则 1**：每个引用参数都有各自的生命周期。
```rust
fn foo<'a, 'b>(x: &'a str, y: &'b str)  // 每个输入引用获得独立生命周期
```

**规则 2**：如果只有一个输入生命周期参数，那么该生命周期被赋给所有输出生命周期参数。
```rust
fn foo<'a>(x: &'a str) -> &'a str  // 输出 = 输入（唯一输入）
```

**规则 3**：如果方法有多个输入生命周期参数，但其中一个是 `&self` 或 `&mut self`，那么 `self` 的生命周期被赋给所有输出生命周期参数。
```rust
impl<'a> Foo<'a> {
    fn bar(&self, other: &str) -> &str { ... }
    // 等价于:
    // fn bar<'b>(&'a self, other: &'b str) -> &'a str
}
```

### 1.6 常见生命周期错误案例

**错误 1：返回悬垂引用**
```rust
// 编译错误：返回的引用指向了局部变量
fn dangle() -> &String {
    let s = String::from("hello");
    &s  // s 在函数结束时被 drop，返回的引用悬垂
}
// 修复：返回 String 而非 &String
fn no_dangle() -> String {
    let s = String::from("hello");
    s  // 所有权转移给调用者
}
```

**错误 2：生命周期约束过紧**
```rust
// 问题：x 和 y 被强制要求相同生命周期，但实际不需要
// fn announce<'a>(x: &'a str, y: &'a str) -> &'a str { ... }
// 对于如下调用：
// let s1 = String::from("long");
// {
//     let s2 = String::from("short");
//     let result = announce(&s1, &s2);  // 错误：s2 生命周期不够长
// }
// 修复：去掉输出
fn announce(x: &str, y: &str) {
    println!("{} and {}", x, y);
}
```

**错误 3：结构体字段生命周期不匹配**
```rust
struct Container<'a> {
    data: &'a str,
}

// 错误：试图将短生命周期的引用存入长生命周期的结构体
// let container;
// {
//     let s = String::from("temp");
//     container = Container { data: &s };  // s 不够长
// }
// container.data;  // 使用已释放的 s
```

### 1.7 子类型（Subtyping）和型变（Variance）基础

这是高级话题，展示对类型系统的深入理解。

**型变规则**：

| 类型参数位置 | 型变 | 含义 |
|------------|------|------|
| `&'a T` | 对 `'a` 协变（covariant） | 更长生命周期是更短生命周期的子类型 |
| `&'a mut T` | 对 `'a` 协变，对 `T` 不变（invariant） | 可变引用禁止读写类型替换 |
| `fn(T) -> U` | 对 `T` 逆变（contravariant），对 `U` 协变 | 函数参数可以接受更泛化的类型 |

**为什么 `&mut T` 对 `T` 是不变的？**

```rust
// 如果 &mut T 对 T 是协变的，以下代码将导致类型安全漏洞：
fn evil(cell: &mut &str) {
    // 假想的协变场景：将更长的引用写入 cell
}

let mut short: &str = "short";
evil(&mut short);  // 如果协变，这里可能写入生命周期更长的引用
```

面试时可以说："我在自己的项目中需要标准库的型变保证来避免这类问题，比如在实现异步 trait 时需要理解 `Pin` 的不变性。"

---

"""
