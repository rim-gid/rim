#include <QtCore/QCoreApplication>

#include "getter.h"

#include <QDebug>

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    qDebug() << "...";

    Getter *getter = new Getter(&a);

    return a.exec();
}
