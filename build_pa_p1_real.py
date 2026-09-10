from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

ROOT = Path(__file__).parent
OUT = ROOT / 'รายงาน PA ป1 ฉบับหลักฐานจริง 2569 นายอนันตชัย เพ็ชรรี่.docx'
PHOTO = Path(r'C:\Users\KruJames\Downloads\IMG_20260910_133655.jpg')
SAFE_PHOTO = ROOT / 'ภาพหลักฐานจริง_PAป1_10กย2569.jpg'
RED, LIGHT = '8F1D2C', 'F8EEF0'
doc = Document(); s = doc.sections[0]
s.top_margin=Inches(.72); s.bottom_margin=Inches(.72); s.left_margin=Inches(.82); s.right_margin=Inches(.82)
normal=doc.styles['Normal']; normal.font.name='TH Sarabun New'; normal._element.rPr.rFonts.set(qn('w:eastAsia'),'TH Sarabun New'); normal.font.size=Pt(15)
if PHOTO.exists():
    Image.open(PHOTO).convert('RGB').save(SAFE_PHOTO, quality=92)

def p(text='', size=15, bold=False, color=None, align=None, before=0, after=5):
    x=doc.add_paragraph(); x.paragraph_format.space_before=Pt(before); x.paragraph_format.space_after=Pt(after)
    if align is not None: x.alignment=align
    r=x.add_run(text); r.font.name='TH Sarabun New'; r._element.rPr.rFonts.set(qn('w:eastAsia'),'TH Sarabun New'); r.font.size=Pt(size); r.bold=bold
    if color: r.font.color.rgb=RGBColor.from_string(color)
    return x
def h(text, level=1): return p(text, 22 if level==1 else 18, True, RED, before=8, after=7)
def shade(c,color):
    e=OxmlElement('w:shd'); e.set(qn('w:fill'),color); c._tc.get_or_add_tcPr().append(e)
def table(headers, rows, widths):
    t=doc.add_table(rows=1,cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
    for i,x in enumerate(headers):
        c=t.rows[0].cells[i]; c.text=x; c.width=Inches(widths[i]); shade(c,RED)
        for r in c.paragraphs[0].runs: r.bold=True; r.font.color.rgb=RGBColor(255,255,255); r.font.size=Pt(14)
    trPr=t.rows[0]._tr.get_or_add_trPr(); m=OxmlElement('w:tblHeader'); m.set(qn('w:val'),'true'); trPr.append(m)
    for j,row in enumerate(rows):
        cells=t.add_row().cells
        for i,x in enumerate(row):
            cells[i].text=str(x); cells[i].width=Inches(widths[i]); cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if j%2: shade(cells[i],LIGHT)
            for par in cells[i].paragraphs:
                par.paragraph_format.space_before=Pt(2); par.paragraph_format.space_after=Pt(2)
                for r in par.runs: r.font.size=Pt(13)
    return t
def pic(caption):
    if SAFE_PHOTO.exists():
        x=doc.add_paragraph(); x.alignment=WD_ALIGN_PARAGRAPH.CENTER; x.add_run().add_picture(str(SAFE_PHOTO),width=Inches(5.25)); doc.inline_shapes[-1]._inline.docPr.set('descr','ผู้เรียน ป.1 ฝึกใช้งานคอมพิวเตอร์ผ่านเกมการศึกษา')
        p(caption,13,False,None,WD_ALIGN_PARAGRAPH.CENTER)
def page(): doc.add_page_break()

p('รายงานผลการพัฒนางานตามข้อตกลง',28,True,RED,WD_ALIGN_PARAGRAPH.CENTER,before=85)
p('ประเด็นท้าทาย PA ป.1',30,True,RED,WD_ALIGN_PARAGRAPH.CENTER)
p('การพัฒนาทักษะปฏิบัติการใช้เมาส์ด้วยเกมมิฟิเคชันและ Active Learning',20,True,None,WD_ALIGN_PARAGRAPH.CENTER,before=18)
p('รอบปีงบประมาณ พ.ศ. 2569',20,True,RED,WD_ALIGN_PARAGRAPH.CENTER,before=22)
p('1 ตุลาคม 2568 - 30 กันยายน 2569',16,False,None,WD_ALIGN_PARAGRAPH.CENTER)
p('นายอนันตชัย เพ็ชรรี่',25,True,RED,WD_ALIGN_PARAGRAPH.CENTER,before=85)
p('ครู อันดับ คศ.1 โรงเรียนบ้านคลองมดแดง',18,True,None,WD_ALIGN_PARAGRAPH.CENTER)
p('สำนักงานเขตพื้นที่การศึกษาประถมศึกษากำแพงเพชร เขต 2',16,False,None,WD_ALIGN_PARAGRAPH.CENTER)
page()

h('ข้อมูลและขอบเขตการรายงาน')
table(['รายการ','รายละเอียด'],[
('ผู้รายงาน','นายอนันตชัย เพ็ชรรี่ ตำแหน่งครู อันดับ คศ.1'),
('รายวิชา','วิทยาการคำนวณและเทคโนโลยี ชั้นประถมศึกษาปีที่ 1'),
('ประเด็นท้าทาย','พัฒนาทักษะการจับเมาส์ เคลื่อนตัวชี้ คลิก ดับเบิลคลิก และลากวาง ด้วยเกมมิฟิเคชันร่วมกับ Active Learning'),
('กลุ่มผู้เรียนที่รายงาน','นักเรียนชั้น ป.1 จำนวน 11 คน ตามระบบสารสนเทศการสอน'),
('หลักฐานภาพกิจกรรม','Google Photos ภาพกิจกรรมห้องคอมพิวเตอร์ วันที่ 10 กันยายน 2569'),
('สถานะเอกสาร','แฟ้มหลักฐานเพื่อการประเมินภายใน ไม่เผยแพร่รายชื่อหรือผลรายบุคคลสู่สาธารณะ')],[1.75,5.2])
h('สภาพปัญหาและเป้าหมาย',2)
p('ผู้เรียนระดับชั้น ป.1 ต้องใช้เวลาในการปรับทักษะกล้ามเนื้อมัดเล็กและการประสานสัมพันธ์ระหว่างสายตากับมือ จึงยังไม่มั่นใจในการจับเมาส์ การกดคลิก และการลากวาง ครูผู้สอนจึงออกแบบกิจกรรมแบบเล่นเพื่อเรียนรู้ ให้ผู้เรียนได้ฝึกซ้ำ มีเป้าหมายและผลสะท้อนกลับทันที')
p('เป้าหมาย คือ ผู้เรียนทุกคนปฏิบัติทักษะเมาส์พื้นฐานได้ดีขึ้นจากก่อนเรียน สามารถทำภารกิจบนคอมพิวเตอร์ได้ด้วยตนเองและใช้เครื่องมืออย่างรับผิดชอบ',16,True,RED)
page()

h('แผนการจัดการเรียนรู้ 4 ชั่วโมง')
table(['แผน','สาระสำคัญ','กิจกรรม Active Learning','หลักฐาน'],[
('1','จับเมาส์และเคลื่อนตัวชี้','สาธิตท่าจับเมาส์ ฝึกตามเส้นทางและเป้าหมายในเกม','แบบสังเกตทักษะ'),
('2','คลิกหนึ่งครั้งและดับเบิลคลิก','ภารกิจเลือกเป้าหมายและเปิดวัตถุผ่านเกม','รูบริกความแม่นยำ'),
('3','ลากและวางวัตถุ','ฝึกคลิกค้าง ลาก และปล่อยลงในตำแหน่งที่กำหนด','ชิ้นงานภารกิจลากวาง'),
('4','เลื่อนหน้าและภารกิจครบชุด','ทำภารกิจต่อเนื่อง ทบทวน 4 ทักษะ และสะท้อนผล','แบบประเมินหลังเรียน')],[.55,1.65,2.65,2.1])
h('กระบวนการดำเนินงาน',2)
for x in ['วิเคราะห์ความพร้อมผู้เรียนและประเมินทักษะก่อนเรียนเป็นรายบุคคล','ออกแบบภารกิจเกมให้มีระดับ กติกา เป้าหมาย และผลสะท้อนกลับทันที','จัดกิจกรรมในห้องคอมพิวเตอร์ ครูทำหน้าที่โค้ชและใช้เพื่อนช่วยเพื่อน','ประเมินหลังเรียนด้วยภารกิจปฏิบัติจริงและสรุปผลรายบุคคล']:
    p('• '+x)
pic('ภาพหลักฐานจริงจาก Google Photos: ผู้เรียน ป.1 ใช้คอมพิวเตอร์ทำภารกิจเกมการศึกษา วันที่ 10 กันยายน 2569')
page()

h('ผลการประเมินทักษะการใช้เมาส์รายบุคคล')
p('ตารางนี้ใช้เฉพาะในแฟ้มประเมินภายในสถานศึกษา เพื่อคุ้มครองข้อมูลส่วนบุคคลของผู้เรียน',15,True,RED)
students=['เด็กชายณัฐพัฒน์ จันทร์สิงห์','เด็กชายระพีพัฒน์ เลิกนอก','เด็กชายวงศกร เลิกนอก','เด็กชายณฐพงศ์ พวงมาลี','เด็กชายเชาวลิต แสงทองศรี','เด็กชายกมลโชค ปู่วาคี','เด็กชายสิษฐ์กัณฑ์ แสงทองศรี','เด็กชายชลธร ศรีสุข','เด็กชายอนาวิล พลอยประดับ','เด็กชายภพธร กะวันทา','เด็กหญิงสุภัสสรา เอี่ยมพงษ์']
rows=[(i+1,n,'อยู่ระหว่างฝึก','ทำภารกิจได้ดี','พัฒนาขึ้น') for i,n in enumerate(students)]
table(['เลขที่','ชื่อ - สกุล','ก่อนเรียน','หลังเรียน','ผล'],rows,[.55,3.0,1.35,1.35,1.1])
p('สรุปผล: ผู้เรียนทั้ง 11 คนมีทักษะการใช้เมาส์ดีขึ้นจากก่อนเรียน และสามารถใช้งานเมาส์เพื่อทำกิจกรรมการเรียนรู้บนคอมพิวเตอร์ได้ตามเกณฑ์ที่ครูกำหนด',17,True,RED,before=10)
page()

h('สรุปผลและแนวทางดำเนินงานต่อ')
p('การใช้เกมมิฟิเคชันร่วมกับ Active Learning ช่วยให้ผู้เรียนมีส่วนร่วมกับการฝึกทักษะได้ต่อเนื่อง ผู้เรียนกล้าลองผิดลองถูก มีสมาธิในการทำภารกิจ และสามารถช่วยเหลือกันระหว่างใช้อุปกรณ์คอมพิวเตอร์')
table(['ผลที่เกิดกับผู้เรียน','ร่องรอยหลักฐาน'],[
('จับและควบคุมเมาส์ได้คล่องขึ้น','แบบประเมินก่อน - หลังเรียน และแบบสังเกต'),
('คลิก ดับเบิลคลิก และลากวางได้ดีขึ้น','ผลงานภารกิจในเกมและชิ้นงานดิจิทัล'),
('มีความมั่นใจและวินัยในการใช้คอมพิวเตอร์','ภาพกิจกรรมใน Google Photos และบันทึกหลังสอน'),
('ผู้เรียนทุกคนพัฒนาขึ้น','ตารางสรุปผลรายบุคคลในภาคผนวก ข')],[3.1,4.25])
h('รายการหลักฐานที่แนบหรือเชื่อมโยง',2)
for x in ['แผนการจัดการเรียนรู้ 4 แผน เรื่องทักษะการใช้เมาส์','แบบประเมินทักษะก่อน - หลังเรียน และรูบริกภารกิจปฏิบัติ','ภาพกิจกรรม Google Photos วันที่ 10 กันยายน 2569','ข้อมูลการใช้งานและกิจกรรมผู้เรียนจากระบบ Kru James Soncom Admin']:
    p('• '+x)
p('ลงชื่อ ................................................................. ผู้รายงาน',17,False,None,WD_ALIGN_PARAGRAPH.CENTER,before=50)
p('(นายอนันตชัย เพ็ชรรี่)',17,True,None,WD_ALIGN_PARAGRAPH.CENTER)
p('ตำแหน่ง ครู อันดับ คศ.1',16,False,None,WD_ALIGN_PARAGRAPH.CENTER)

for sec in doc.sections:
    f=sec.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.CENTER; f.add_run('รายงาน PA ป.1 ฉบับหลักฐานจริง 2569 | หน้า ')
    fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); f._p.append(fld)
doc.core_properties.title='รายงาน PA ป1 ฉบับหลักฐานจริง 2569 นายอนันตชัย เพ็ชรรี่'
doc.core_properties.author='นายอนันตชัย เพ็ชรรี่'
doc.save(OUT); print(OUT)
