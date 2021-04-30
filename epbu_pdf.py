import os,re,unicodedata,zipfile,fitz,glob,shutil
from lxml import etree
path=[]

def findAllFile(base):
    # print(base)
    for root, dirs, files in os.walk(base, topdown=False):
        for name in files:
            local = os.path.join(root, name)
            html_id.append(name)

# 重名jpg
def Epub_jpg(route):
    global html_id
    html_id = []
    img_id = []
    findAllFile('%s\html'%route)
    html_id.sort()
    # print(html_id)
    for index,i in enumerate(html_id):
        selector = etree.HTML(open(route+'\html\\'+i,encoding='utf-8').read())
        content = selector.xpath('/html/body/div/div/img/@src')
        # print(i)
        # print(route+content[0][2:])
        # print(route+'/image/%s.%s'%(i[:-5].zfill(10),content[0][-3:]))
        try:
            os.rename(route+content[0][2:],route+'/image/%s.%s'%(i[:-5].zfill(10),content[0][-3:]))
        except Exception as e:
            print(e)

# epub解压
def Unzip(path):
    try:
        os.mkdir(path)
    except:
        pass
    z = zipfile.ZipFile('%s' % path, 'r')
    z.extractall(CacheDirectory)

# 图片转pdf
def pic2pdf(img_dir,Pdf_name):
    doc = fitz.open()
    for img in sorted(glob.glob("{}/*".format(img_dir))):  # 读取图片，确保按文件名排序
        print(img)
        imgdoc = fitz.open(img)  # 打开图片
        pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)  # 将当前页插入文档
    if os.path.exists(PdfStorageDirectory+Pdf_name+'.pdf'):
        os.remove(PdfStorageDirectory+Pdf_name+'.pdf')
    doc.save(PdfStorageDirectory+"%s.pdf"%Pdf_name)  # 保存pdf文件
    doc.close()

def start(path,name):
    # try:
    #     shutil.rmtree(CacheDirectory)
    # except:
    #     pass
    Unzip(path)
    Epub_jpg(CacheDirectory)
    pic2pdf(CacheDirectory+"\image",name)
    # shutil.rmtree(CacheDirectory)

if __name__ == '__main__':
    FileDirectory = r'E:\BaiduNetdiskDownload\鬼灭'
    CacheDirectory = r'E:\BaiduNetdiskDownload\00'
    PdfStorageDirectory = '.'
    # 更换epub文件夹目录
    for root, dirs, files in os.walk(FileDirectory, topdown=False):
        for name in files:
            local = os.path.join(root, name)
            path.append(local)
    # 切片pdf昵称
    for i in path:
        print(i[27:-5])
        start(i,i[27:-5])
