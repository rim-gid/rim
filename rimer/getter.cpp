#include "getter.h"

#include <QNetworkAccessManager>
#include <QDebug>

Getter::Getter(QObject *parent) :
    QObject(parent)
{
    qDebug() << "start";

    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    connect(manager, SIGNAL(finished(QNetworkReply*)),this, SLOT(replyFinished(QNetworkReply*)));

    manager->get(QNetworkRequest(QUrl("http://qt.nokia.com")));

    QNetworkRequest request;
    request.setUrl(QUrl("http://rim-gid.ru"));
    request.setRawHeader("User-Agent", "MyOwnBrowser 1.0");

    QNetworkReply *reply = manager->get(request);
    connect(reply, SIGNAL(readyRead()), this, SLOT(slotReadyRead()));
    connect(reply, SIGNAL(error(QNetworkReply::NetworkError)),this, SLOT(slotError(QNetworkReply::NetworkError)));
    connect(reply, SIGNAL(sslErrors(QList<QSslError>)),this, SLOT(slotSslErrors(QList<QSslError>)));
}

void Getter::replyFinished(QNetworkReply*) {
    qDebug() << "replyFinished";
}

void Getter::slotReadyRead() {
    qDebug() << "slotReadyRead";
}

void Getter::slotError(QNetworkReply::NetworkError) {
    qDebug() << "slotError";
}

void Getter::slotSslErrors(QList<QSslError>) {
    qDebug() << "slotSslErrors";
}
