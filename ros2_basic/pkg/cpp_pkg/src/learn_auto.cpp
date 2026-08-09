#include "iostream"

int main()
{
    auto a = 10;                        // 使用auto关键字自动推导变量类型为int
    auto b = 3.14f;                     // 自动推导为float
    auto c = "Hello";                   // 自动推导为const char*

    std::cout << "a: " << a << ", b: " << b << ", c: " << c << std::endl;
    return 0;
}