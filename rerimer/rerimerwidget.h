#ifndef RERIMERWIDGET_H
#define RERIMERWIDGET_H

#include <QWidget>

namespace Ui {
    class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = 0);
    ~Widget();

private slots:
    void on_pushButton_clicked();

    void on_textEdit_textChanged();

    void on_listWidget_currentTextChanged(const QString &currentText);

private:
    Ui::Widget *ui;
};

#endif // RERIMERWIDGET_H
