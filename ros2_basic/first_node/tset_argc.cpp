#include <iostream>

int main(int argc, char * argv[])
{
  std::cout << "参数个数: " << argc << std::endl;
  std::cout << "程序名称: " << argv[0] << std::endl;
  std::string str = argv[1];
  if(str == "--help") {
    std::cout << "帮助信息" << std::endl;
  };
  return 0;
}