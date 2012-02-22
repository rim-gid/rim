/****************************************************************************
** Meta object code from reading C++ file 'getter.h'
**
** Created: Thu Nov 24 12:57:07 2011
**      by: The Qt Meta Object Compiler version 62 (Qt 4.7.4)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "getter.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'getter.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.7.4. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_Getter[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
       4,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: signature, parameters, type, tag, flags
       8,    7,    7,    7, 0x0a,
      38,    7,    7,    7, 0x0a,
      54,    7,    7,    7, 0x0a,
      93,    7,    7,    7, 0x0a,

       0        // eod
};

static const char qt_meta_stringdata_Getter[] = {
    "Getter\0\0replyFinished(QNetworkReply*)\0"
    "slotReadyRead()\0slotError(QNetworkReply::NetworkError)\0"
    "slotSslErrors(QList<QSslError>)\0"
};

const QMetaObject Getter::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_Getter,
      qt_meta_data_Getter, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &Getter::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *Getter::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *Getter::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_Getter))
        return static_cast<void*>(const_cast< Getter*>(this));
    return QObject::qt_metacast(_clname);
}

int Getter::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: replyFinished((*reinterpret_cast< QNetworkReply*(*)>(_a[1]))); break;
        case 1: slotReadyRead(); break;
        case 2: slotError((*reinterpret_cast< QNetworkReply::NetworkError(*)>(_a[1]))); break;
        case 3: slotSslErrors((*reinterpret_cast< QList<QSslError>(*)>(_a[1]))); break;
        default: ;
        }
        _id -= 4;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
