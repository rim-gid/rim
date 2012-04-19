var theSelection = false;

var clientPC = navigator.userAgent.toLowerCase();
var clientVer = parseInt(navigator.appVersion);

var is_ie = ((clientPC.indexOf("msie") != -1) && (clientPC.indexOf("opera") == -1));
var is_win = ((clientPC.indexOf("win")!=-1) || (clientPC.indexOf("16bit") != -1));

helplines = new Array(
 "�����: &lt;p&gt;�����&lt;/p&gt;",
 "������� ������: &lt;br&gt;�����",
 "������ �����: &lt;b&gt;�����&lt;/b&gt;",
 "��������� �����: &lt;i&gt;�����&lt;/i&gt;",
 "������������ �����: &lt;u&gt;�����&lt;/u&gt;",
 "������������� �����: &lt;s&gt;�����&lt;/s&gt;",
 "������ ������: &lt;sub&gt;�����&lt;/sub&gt;",
 "������� ������: &lt;sup&gt;�����&lt;/sup&gt;",
 "������������: &lt;div align=center&gt;�����&lt;/div&gt;",
 "���� ������: &lt;font color=red&gt;�����&lt;/font&gt;  ���������: ��� color=#FF0000",
 "���: &lt;code&gt;�����&lt;/code&gt;",
 "������� (���������): &lt;pre&gt;���&lt;/pre&gt;",
 "������: &lt;blockquote&gt;�����&lt;/blockquote&gt;",
 "����� &lt; � &gt; � ������ ��������",
 "������������� ������: &lt;ul&gt;�����&lt;/ul&gt;",
 "������������ ������: &lt;ol&gt;�����&lt;/ol&gt;",
 "����� ��� ������ � ������: &lt;li&gt;�����",
 "�������� ��������: &lt;img src=http://image_url&gt;",
 "�������� ������: &lt;a href=http://url&gt;����� ������&lt;/a&gt;",
 "����� E-mail: &lt;a href=mailto:E-mail&gt;E-mail&lt;/a&gt;"
);

bbcode = new Array();
bbtags = new Array(
 '<p>','', //0  !!! ����� ������ ���. � ����
 '<br>','', //2
 '<b>','</b>',
 '<i>','</i>',
 '<u>','</u>',
 '<s>','</s>',
 '<sub>','</sub>',
 '<sup>','</sup>',
 '<div align="center">','</div>',
 '<font color="red">','</font>',
 '<code>','</code>',
 '<pre>','</pre>',
 '<blockquote>','</blockquote>',
 '&lt;','&gt;',
 '<ul>','</ul>',
 '<ol>','</ol>',
 '<li>','', //32
 '<img src="" hspace="2" vspace="2" title="">','', //34
 '<a href="" target="_blank">','</a>',
 '<a href="mailto:">','</a>' //38
);

function not_closed_tags(n) {
 var r=false;
 if (n==0 || n==2 || n==32 || n==34) r=true;
 return r;
}

function helpline (i) {
 if (i<0) document.getElementById('helpbox').innerHTML =  '����� ������ ��������� ����� � ����������� ������';
 else document.getElementById('helpbox').innerHTML =  helplines[i];
}

function getarraysize(thearray) {
 for (i = 0; i < thearray.length; i++) {
  if ((thearray[i] == "undefined") || (thearray[i] == "") || (thearray[i] == null)) return i;
 }
 return thearray.length;
}

function arraypush(thearray,value) {
 thearray[ getarraysize(thearray) ] = value;
}

function arraypop(thearray) {
 thearraysize = getarraysize(thearray);
 retval = thearray[thearraysize - 1];
 delete thearray[thearraysize - 1];
 return retval;
}

function bbplace(text) {
 var txtarea = document.f1.text;
 var scrollTop = (typeof(txtarea.scrollTop) == 'number' ? txtarea.scrollTop : -1);
 if (txtarea.createTextRange && txtarea.caretPos) {
  var caretPos = txtarea.caretPos;
  caretPos.text = caretPos.text.charAt(caretPos.text.length - 1) == ' ' ? caretPos.text + text + ' ' : caretPos.text + text;
  txtarea.focus();
 } 
 else if (txtarea.selectionStart || txtarea.selectionStart == '0') {
  var startPos = txtarea.selectionStart;
  var endPos = txtarea.selectionEnd;
  txtarea.value = txtarea.value.substring(0, startPos) + text + txtarea.value.substring(endPos, txtarea.value.length);
  txtarea.focus();
  txtarea.selectionStart = startPos + text.length;
  txtarea.selectionEnd = startPos + text.length;
 }
 else {
  txtarea.value  += text;
  txtarea.focus();
 }
 if (scrollTop >= 0 ) { txtarea.scrollTop = scrollTop; }
}

function bbstyle(bbnumber) {
 var txtarea = document.f1.text;
 txtarea.focus();
 donotinsert = false;
 theSelection = false;
 bblast = 0;
 if (bbnumber == -1) { //������� ��� ���
  while (bbcode[0]) {
   butnumber = arraypop(bbcode) - 1;
   txtarea.value += bbtags[butnumber + 1];
  }
  txtarea.focus();
  return;
 }
 if ((clientVer >= 4) && is_ie && is_win) {
  theSelection = document.selection.createRange().text; //�������� ��������� ��� IE
  if (theSelection) { //�������� ���� ������ ��������� ���������
   document.selection.createRange().text = bbtags[bbnumber] + theSelection + bbtags[bbnumber+1];
   txtarea.focus();
   theSelection = '';
   return;
  }
 }
 else if (txtarea.selectionEnd && (txtarea.selectionEnd - txtarea.selectionStart > 0)) {
  //�������� ��������� ��� Mozilla
  mozWrap(txtarea, bbtags[bbnumber], bbtags[bbnumber+1]);
  return;
 }
 for (i = 0; i < bbcode.length; i++) {
  if (bbcode[i] == bbnumber+1 && !not_closed_tags(bbnumber)) { 
   bblast = i;
   donotinsert = true;
  }
 }
 if (donotinsert) {
  while (bbcode[bblast]) {
   butnumber = arraypop(bbcode) - 1;
   if (!not_closed_tags(butnumber)) bbplace(bbtags[butnumber + 1]);
  }
  txtarea.focus();
  return;
 } 
 else { //������� ���
  bbplace(bbtags[bbnumber]);
  arraypush(bbcode,bbnumber+1);
  txtarea.focus();
  return;
 }
 storeCaret(txtarea);
}

function mozWrap(txtarea, open, close) {
 if (txtarea.selectionEnd > txtarea.value.length) { txtarea.selectionEnd = txtarea.value.length; }
 var oldPos = txtarea.scrollTop;
 var oldHght = txtarea.scrollHeight;
 var selStart = txtarea.selectionStart;
 var selEnd = txtarea.selectionEnd+open.length;
 txtarea.value = txtarea.value.slice(0,selStart)+open+txtarea.value.slice(selStart); 
 txtarea.value = txtarea.value.slice(0,selEnd)+close+txtarea.value.slice(selEnd);
 txtarea.selectionStart = selStart+open.length;
 txtarea.selectionEnd = selEnd;
 var newHght = txtarea.scrollHeight - oldHght;
 txtarea.scrollTop = oldPos + newHght;
 txtarea.focus();
}

function storeCaret(textEl) { //������� � ������� ������� - ���� ��� IE
 if (textEl.createTextRange) textEl.caretPos = document.selection.createRange().duplicate();
 document.getElementById('helpbox').innerHTML = "�����: "+ document.f1.text.value.length;
}

function showIcons () {
 var l=bbtags.length;
 for (i=0; i<l; i+=2) {
  var p = bbtags[i].indexOf(' ');
  if (p<0) p = bbtags[i].indexOf('>');
  if (p<0) p = bbtags[i].indexOf(';');
  var tagname = bbtags[i].substring (1,p);
  if (i==38) tagname='am';
  var i2= i/2;
  var alter= helplines[i2];
  document.writeln ('<img src="tags/'+tagname+'.gif" width="16" height="16" hspace="0" vspace="0" alt="'+alter+'" title="'+alter+'"  onClick="bbstyle('+i+')" onMouseOver="helpline('+i2+')" onMouseOut="helpline(-1)">');
  if (i==14 || i==26 || i==32) document.writeln ('&nbsp;&nbsp;&nbsp;');
 }
}

var maxLen=1024;
var maxWordLen=80;

function strip_tags (string) {
 return string.replace(/<\/?[^>]+>/gi, '');  
} 

function trim(string) {
 return string.replace (/(^\s+)|(\s+$)/g, "");
}

function goodWordsLength (v) {
 var s=v.split(/\s/);
 for (var i=0; i<s.length; i++) 
  if (s[i].length>maxWordLen) {
   return false;
  }
 return true;
}

function checkblock() {
 var text=strip_tags(trim(document.f1.text.value));
 if (text=='') {
  window.alert (
   '����� ����� �� ����� ���� ������, ����������, ��������� ���');
  return false;
 }
 if (text.length > maxLen) {
  window.alert (
   '����� ������� �������. ���������� �����: '+ maxLen);
  return false;
 }
 if (goodWordsLength(text)==false) {
  window.alert (
   '� ������ ���� ������� ������� �����. ���������� �����: '+
    maxWordLen);
  return false;
 }
 return true;
}