#include <iostream>
#include <algorithm>

int main(){
    auto add = [](int a,int b){return a+b;}; // 定义一个lambda表达式，接受两个整数参数，返回它们的和    
    int sum = add(3,5); // 调用lambda表达式，计算3和5的和
    auto print_sum = [sum/*可以填入&*/]() -> void
    {std::cout << "Sum: " << sum << std::endl;}; // 定义一个lambda表达式，打印两个整数的和

    print_sum(); // 调用lambda表达式，打印3和5的和
    return 0;
}