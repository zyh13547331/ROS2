#include <iostream>
#include <memory>

int main()
{
    auto p1 = std::make_shared<std::string>("Hello, World!"); // 创建一个共享指针，指向一个字符串对象
    /*std::make_shared<数据类型/类>(参数列表);返回值，对应类的共享指针std::shared_ptr<std::string>可以直接写为auto p1*/
    std::cout << "p1的引用计数: " << p1.use_count()<<"内存地址: " << p1.get() << std::endl; // 1
    auto p2 = p1; // 复制共享指针，引用计数增加
    std::cout << "p1的引用计数: " << p1.use_count()<<"内存地址: " << p1.get() << std::endl; // 2
    std::cout << "p2的引用计数: " << p2.use_count()<<"内存地址: " << p2.get() << std::endl; // 2

    p1.reset(); // 重置p1，引用计数减少,不指向内存
    std::cout << "p1的引用计数: " << p1.use_count()<<"内存地址: " << p1.get() << std::endl; // 0
    std::cout << "p2的引用计数: " << p2.use_count()<<"内存地址: " << p2.get() << std::endl; // 1

    std::cout << "p2的值: " << *p2 << std::endl; // 输出共享指针指向的字符串内容
    return 0;
}