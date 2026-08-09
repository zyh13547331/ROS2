#include <iostream>
#include <functional>

/*自由函数*/
void save_with_free_fun(const std::string &filename)
{
    std::cout << "自由函数: " << filename << std::endl;
}

/*成员函数*/
class FileSaver
{
private:
    /*data*/
public:
    FileSaver(/* args */) = default;
    ~FileSaver() = default;

    void save_with_member_fun(const std::string &filename)
    {
        std::cout << "成员方法: " << filename << std::endl;
    }
};

int main()
{
    FileSaver fileSaver;
    /*lambda函数*/

    auto save_with_lambda = [](const std::string &filename) ->void
    {
        std::cout << "lambda函数: " << filename << std::endl;
    };

    std::function<void(const std::string &)> save1 = save_with_free_fun; // 绑定自由函数
    std::function<void(const std::string &)> save2 = std::bind(&FileSaver::save_with_member_fun, &fileSaver, std::placeholders::_1); // 绑定成员函数
    std::function<void(const std::string &)> save3 = save_with_lambda; // 绑定lambda函数


    save1("file1.txt");
    save2("file2.txt");
    save3("file3.txt");
    return 0;
}