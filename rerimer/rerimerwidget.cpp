#include "rerimerwidget.h"
#include "ui_rerimerwidget.h"

#include "QDebug"
#include "QDomNode"
#include "QDomDocument"
#include "QDir"
#include <QTextCodec>

const QString VKS = "<!-- / vkontakte share button -->";
const QString SOME_FIN = "<!--/post";
const QString SOME_ATA = "attachment";
const QString ATA_START = "<div";
const QString ATA_STOP = "</div>";

const QString IMG_TITLE= "title=\"";
const QString IMG_TITLE_STOP= "\" w";
const QString IMG_CAPTION= "wp-caption-text\">";
const QString IMG_CAPTION_STOP= "</p>";

const QString DEFAULT_DIR= "/home/andrey/Documents/";

const QString RUS_ALPHA= "�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�|�";
const QString EN_ALPHA = "a|b|v|g|d|e|yo|zh|z|i|iy|k|l|m|n|o|p|r|s|t|u|f|h|c|ch|sh|sh|i|i|i|e|yu|ya|A|B|V|G|D|E|YO|ZH|Z|I|IY|K|L|M|N|O|P|R|S|T|U|F|H|C|CH|SH|SH|I|I|I|E|YU|YA";

QStringList RUS_ALPHA_list;
QStringList EN_ALPHA_list;

QString rez;
QString filename;
QStringList titles;
QStringList captions;

QMap<QString,int> titlePos;
QMap<QString,int> captionPos;

QStringList freetitles;
QStringList freecaptions;
QMap<QString,QString> titlesMap;
QMap<QString,QString> captionsMap;

bool createdTranDir = false;
QDir transDir;

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);

    QDir dir(DEFAULT_DIR);
    QStringList nms;
    nms << "*.html";
    QStringList list = dir.entryList(nms);

    qDebug() << list;
    ui->listWidget->addItems(list);

}

Widget::~Widget()
{
    delete ui;
}

QString translitRUEN(char ch) {
    switch (ch) {
        case '�': return "a"; break;
        case '�': return "b"; break;
        case '�': return "v"; break;
        case '�': return "g"; break;
        case '�': return "d"; break;
        case '�': return "e"; break;
        case '�': return "eo"; break;
        case '�': return "zh"; break;
        case '�': return "z"; break;
        case '�': return "i"; break;
        case '�': return "iy"; break;
        case '�': return "k"; break;
        case '�': return "l"; break;
        case '�': return "m"; break;
        case '�': return "n"; break;
        case '�': return "o"; break;
        case '�': return "p"; break;
        case '�': return "r"; break;
        case '�': return "s"; break;
        case '�': return "t"; break;
        case '�': return "u"; break;
        case '�': return "f"; break;
        case '�': return "h"; break;
        case '�': return "c"; break;
        case '�': return "ch"; break;
        case '�': return "sh"; break;
        case '�': return "sh"; break;
        case '�': return "i"; break;
        case '�': return "i"; break;
        case '�': return "e"; break;
        case '�': return "yu"; break;
        case '�': return "ya"; break;

        case '�': return "A"; break;
        case '�': return "B"; break;
        case '�': return "V"; break;
        case '�': return "G"; break;
        case '�': return "D"; break;
        case '�': return "E"; break;
        case '�': return "EO"; break;
        case '�': return "ZH"; break;
        case '�': return "Z"; break;
        case '�': return "I"; break;
        case '�': return "IY"; break;
        case '�': return "K"; break;
        case '�': return "L"; break;
        case '�': return "M"; break;
        case '�': return "N"; break;
        case '�': return "O"; break;
        case '�': return "P"; break;
        case '�': return "R"; break;
        case '�': return "S"; break;
        case '�': return "T"; break;
        case '�': return "U"; break;
        case '�': return "F"; break;
        case '�': return "H"; break;
        case '�': return "C"; break;
        case '�': return "CH"; break;
        case '�': return "SH"; break;
        case '�': return "SH"; break;
        case '�': return "I"; break;
        case '�': return "I"; break;
        case '�': return "E"; break;
        case '�': return "YU"; break;
        case '�': return "YA"; break;
        default: QString s; s.append( QChar(ch) ); return s; break;
    }
}

QString translitRUEN(QString &s, bool *changed = 0) {
    QString rez;
    bool cha = false;
    if (RUS_ALPHA_list.length() == 0) {
        QTextCodec *codec2 = QTextCodec::codecForLocale();
        QByteArray ar;
        ar.append(RUS_ALPHA);
        QString ss = codec2->toUnicode(ar);
        RUS_ALPHA_list = ss.split("|");
        EN_ALPHA_list = EN_ALPHA.split("|");
    }

    for (int i = 0; i < s.length(); ++i) {
       QString t = QString(s.at(i));
       int ind = RUS_ALPHA_list.indexOf(t);
       if (ind == -1) {
           rez.append(t);
       } else {
           rez.append(EN_ALPHA_list[ind]);
           cha = true;
       }
    }
    if (cha) {
        if (changed) {
            *changed = true;
        }
    }
    return rez;
}

QString getImgTitle(QString& s) {
    int a = s.indexOf(IMG_TITLE);
    if (a<0) return "";
    int b = s.indexOf(IMG_TITLE_STOP,a);
    if (b<0) return "";
    QString ttl = s.mid(a+IMG_TITLE.length(),b-a-IMG_TITLE.length());
    return ttl;
}

QString getImgCapthion(QString& s) {
    int a = s.indexOf(IMG_CAPTION);
    if (a<0) return "";
    int b = s.indexOf(IMG_CAPTION_STOP,a);
    if (b<0) return "";
    return s.mid(a+IMG_CAPTION.length(),b-a-IMG_CAPTION.length());
}

void cutATA(QString& s, int start=0) {
    int a = s.indexOf(SOME_ATA,start);
    if (a<0) return;
    int b = s.lastIndexOf(ATA_START,a);
    if (b<0) return;
    int c = s.indexOf(ATA_STOP,a);
    if (c<0) return;
    QString mid = s.mid(b,c-b+ATA_STOP.length());
    qDebug() << a << c << mid;

    //QString newmid = getImg(mid);

    QString ttl = getImgTitle(mid); ttl = translitRUEN(ttl);
    QString cpth = getImgCapthion(mid);

    ttl.replace("-","_");
    ttl.replace(" ","_");
    //cpth.replace("-","_");

    titles.append(ttl);
    captions.append(cpth);

    titlePos[ttl] = b;
    titlePos[cpth] = b;

    QString zz ="<img src='/" + ttl + ".jpg' align='left' vspace='5' hspace='5'/>";
    QString dd = "<a>"+cpth+"</a>";

    s.replace(mid,"\n\n"+zz+dd+"\n\n");

    //rez += "\n_______\n" + mid + "\n_______\n";

    cutATA(s, b);
}

void seeChilds(QDomNode &doc) {
    for (int i = 0; i < doc.childNodes().count(); ++i) {
        QDomNode nd = doc.childNodes().at(i);
        qDebug() << "***" << i  << "childes =" << nd.childNodes().count() << "***\n" << nd.nodeName() << nd.nodeValue();
        seeChilds(nd);
    }
}

void seePost(QString& s, int start=0) {
    int a = s.indexOf(VKS,start);
    if (a<0) return;
    int b = s.indexOf(SOME_FIN,a);
    if (b<0) return;
    QString mid = s.mid(a+VKS.length(),b-a-VKS.length());
    qDebug() << a << b << mid;

    cutATA(mid);

    rez += "\n_______\n" + mid + "\n_______\n";
}

void seeNextBig(QString& s, int last=0) {
    int a = s.indexOf("<big>",last);
    if (a<0) return;
    int b = s.indexOf("</big>",a);
    if (b<0) return;
    QString mid = s.mid(a+5,b-a-5);
    qDebug() << a << b << mid;
    rez += "\n_______\n" + mid + "\n_______\n";
    seePost(s, b);
    seeNextBig(s, b);
}

void Widget::on_pushButton_clicked()
{
}

void Widget::on_textEdit_textChanged()
{
    rez.clear();
    titles.clear();
    captions.clear();

    titlePos.clear();
    captionPos.clear();

    freetitles.clear();
    freecaptions.clear();
    titlesMap.clear();
    captionsMap.clear();

    createdTranDir = false;

    QString s = ui->textEdit->toPlainText();
    s = s.simplified();
    seeNextBig(s);

    ui->textEdit_2->setPlainText(rez);
}

bool findTextInRez(QString& s) {
    if (rez.indexOf(s) != -1) return true;
    else return false;
}

void copyTranslited(const QString &filesDir,const QString &fileName, const QString &translited) {
    if (!createdTranDir) {
        createdTranDir = true;
        transDir = QDir(filesDir+"_TRANSLITED");
        if (!transDir.exists()) {
            transDir.mkdir(filesDir+"_TRANSLITED");
        }
    }
    QFile file(filesDir+"/"+fileName);
    QFile fileOut(filesDir+"_TRANSLITED/"+translited);
    if (file.open(QFile::ReadOnly)) {
        if (fileOut.open(QFile::WriteOnly)) {
            QByteArray ar = file.readAll();
            fileOut.write(ar);
        }
    }
    file.close();
    fileOut.close();
}

void Widget::on_listWidget_currentTextChanged(const QString &currentText)
{
    filename = DEFAULT_DIR+currentText;
    QFile file(DEFAULT_DIR+currentText);
    if (file.open(QFile::ReadOnly)) {
        QByteArray ar = file.readAll();
        QTextCodec *codec = QTextCodec::codecForName("UTF8");
        QString s = codec->toUnicode(ar);
        //QTextCodec *codec2 = QTextCodec::codecForName("KOI8-R");
        //codec2->fromUnicode(s);
        ui->textEdit->setPlainText( s );
    } else {
        ui->textEdit->setPlainText("NOT READED...");
    }

    ui->listWidget_2->clear();
    QString s = DEFAULT_DIR+currentText;
    if (s.right(4)=="html") {
      QString s1 = s.left(s.length()-5)+"_files";
      QDir dir(s1);
      if (dir.exists()) {
          QStringList jpgs;
          jpgs << "*.jpg" << "*.jpeg";
          QStringList list = dir.entryList(jpgs);
          for (int k=0; k<list.count();++k) {
              bool cha = false;
              QString ts = list[k];
              list[k] = translitRUEN(ts,&cha);
              if (cha) {
                  qDebug() << ts << ">>" << list[k];
                  copyTranslited(s1,ts,list[k]);
              }
          }
          //list.removeAll(".");
          //list.removeAll("..");
          ui->listWidget_2->addItems(list);
          for (int i = 0; i < ui->listWidget_2->count(); ++i) {
              QListWidgetItem *item = ui->listWidget_2->item(i);
              QString ss = item->text().replace("-","_");
              ss = ss.left(ss.length()-4);
              if (findTextInRez(ss)) {
                  item->setBackgroundColor(QColor(0,190,0));
              }
              /*if ( ui->textEdit_2->find(ss) ) {
                  QTextCursor cur = ui->textEdit_2->textCursor();
                  int pos = cur.position();
                  cur.setPosition(pos+ss.length());
                  ui->textEdit_2->insertHtml("</span>");
                  cur.setPosition(pos);
                  ui->textEdit_2->insertHtml("<span style='color:#009900;'>");
              }*/

              QTextCursor newCursor(ui->textEdit_2->document());
              QTextCharFormat colorFormat;
              colorFormat.setBackground(QBrush(QColor(0,190,0)));
               while (!newCursor.isNull() && !newCursor.atEnd()) {
                   newCursor = ui->textEdit_2->document()->find(ss, newCursor);

                   if (!newCursor.isNull()) {
                       //newCursor.setPosition(newCursor.position()+2,QTextCursor::KeepAnchor);
                       //newCursor.movePosition(QTextCursor::WordRight,QTextCursor::KeepAnchor);
                       newCursor.mergeCharFormat(colorFormat);
                   }
               }


          }
      }

      if (createdTranDir) {
          QFile file4(s1+"_TRANSLITED/index.html");
          if (file4.open(QFile::WriteOnly)) {
              QTextCodec *codec = QTextCodec::codecForName("UTF8");
              QByteArray ar = codec->fromUnicode(ui->textEdit_2->toPlainText());
              file4.write(ar);
          }
          file4.close();
      }


    }



    /*QStringList nms;
    nms << "*.html";
    QStringList list = dir.entryList(nms);

    qDebug() << list;
    ui->listWidget->addItems(list);*/
}
