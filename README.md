Rust Internal Registry
======================

RIR is a simple idea (POC) how you can generate a internal Rust Registry based under a Cargo.lock File

### Requirements:

- Cargo
- [Cargo Local Registry](https://github.com/ChrisGreenaway/cargo-local-registry)

### How to Start

Install Dependencies

~~~sh
$ make install & make deps
~~~

Start API

~~~sh
$ make play
~~~

In other terminal, Build Repository Cache

~~~sh
$ make example
~~~


### Configure Cargo

~~~sh
curl http://localhost:8080/api/v1/rust-registry-index/cargo > ~/.cargo/config
~~~

And now build you project...


