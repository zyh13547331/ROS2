#include <QApplication>
#include <QLabel>
#include <QString>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QString message = "Hello, Qt!";
    QLabel label(message);
    label.setAlignment(Qt::AlignCenter);
    label.resize(400, 200);
    label.show();

    return app.exec();
}