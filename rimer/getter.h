#ifndef GETTER_H
#define GETTER_H

#include <QObject>
#include <QNetworkReply>
#include <QSslError>

class Getter : public QObject
{
    Q_OBJECT
public:
    explicit Getter(QObject *parent = 0);

signals:

public slots:
    void replyFinished(QNetworkReply*);
    void slotReadyRead();
    void slotError(QNetworkReply::NetworkError);
    void slotSslErrors(QList<QSslError>);
};

#endif // GETTER_H
