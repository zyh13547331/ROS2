#include <iostream>
#include <thread> /*多线程*/
#include <chrono> /*时间*/
#include <functional> /*函数对象*/
#include <httplib.h> /*http请求*/

class DownLoad{
    private:
    /**/
    public:
        void download(const std::string &host, const std::string &path, const std::function
            <void(const std::string&,const std::string&)> &callback_count)
            {
                std::cout << "线程" << std::this_thread::get_id() << "开始下载" << path << std::endl;
                httplib::Client cli(host.c_str());
                auto res = cli.Get(path.c_str());
                if (res && res->status == 200) {
                    std::cout << "线程" << std::this_thread::get_id() << "下载完成" << path << std::endl;
                    callback_count(host, res->body);
                } else {
                    std::cout << "线程" << std::this_thread::get_id() << "下载失败" << path << std::endl;
                }
            };

        void start_download(const std::string &host, const std::string &path, const std::function
            <void(const std::string&,const std::string&)> &callback_count)
            {
                auto fun = std::bind (&DownLoad::download,this,std::placeholders::_1,
                std::placeholders::_2,std::placeholders::_3);
                std::thread t(fun, host , path, callback_count);
                t.detach();
            };
};

int main()
{
    auto download = DownLoad();
    auto callback_count = [](const std::string &path, const std::string &result) ->void {
        std::cout << "下载完成" << path <<":"<< result.length() << result.substr(0,5)<<std::endl; 
    };
    download.start_download("http://localhost:8000","/nocel1.txt", callback_count);
    download.start_download("http://localhost:8000","/nocel2.txt", callback_count);
    download.start_download("http://localhost:8000","/nocel3.txt", callback_count);

    std::this_thread::sleep_for(std::chrono::seconds(10));

    return 0;
}

