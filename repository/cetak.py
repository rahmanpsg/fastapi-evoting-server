from datetime import datetime, date, time
import os
from fpdf import FPDF
from sqlalchemy.orm import Session
from models.daftar_vote import DaftarVotes

from models.kandidat import Kandidats
from models.pemilih import Pemilihs

import urllib.request as req

def cetak_kandidat(db: Session):
    path = 'assets/kandidat.pdf'
    cloud_name = os.getenv('CLOUD_NAME')
    pdf = FPDF()
    pdf.add_page(orientation="landscape", format="LEGAL")

    TABLE_COL_NAMES = ("No", "Foto", "Nama", "Keterangan")

    kandidats = db.query(Kandidats).all()

    TABLE_DATA = ((str(idx+1), kandidat.foto, kandidat.nama, kandidat.keterangan)
                  for idx, kandidat in enumerate(kandidats))    

    pdf.set_font("Times", size=16)
    line_height = pdf.font_size * 2

    TABLE_COL_WIDTH = [10.0, 50.0, 80.0, 200.0]

    render_table_header(pdf, TABLE_COL_NAMES,TABLE_COL_WIDTH, line_height)

    for row in TABLE_DATA:
        if pdf.will_page_break(line_height):
            render_table_header(pdf, TABLE_COL_NAMES,TABLE_COL_WIDTH, line_height)
        y = pdf.get_y()
        lh = max([(pdf.get_string_width(data)/TABLE_COL_WIDTH[idx])*8 for idx, data in enumerate(row)]);


        for idx, data in enumerate(row):            
            if idx == 1:
                pdf.cell(TABLE_COL_WIDTH[idx], lh,  border=1)
                y = pdf.get_y()

                x = pdf.get_x()
                pdf.image(
                    f"https://res.cloudinary.com/{cloud_name}/image/upload/q_auto:low,w_100,h_100/{data}", h=20, w=20, x=35, y=y+(lh/6))
                pdf.set_y(y)
                pdf.set_x(x)

            elif idx == 3:                                
                pdf.multi_cell(TABLE_COL_WIDTH[idx], lh,
                     data, border=1, align="C", max_line_height=6,ln=0 if len(row) != idx+1 else 1)
            else:
                pdf.cell(TABLE_COL_WIDTH[idx], lh, data, border=1, align="C")

    pdf.output(path)
    return path


def cetak_pemilih(db: Session):
    path = 'assets/pemilih.pdf'
    cloud_name = os.getenv('CLOUD_NAME')

    pdf = FPDF()
    pdf.add_page(orientation="landscape", format="LEGAL")

    TABLE_COL_NAMES = ("NO","FOTO", "NAMA", "NIK", "USERNAME", "ALAMAT", "STATUS")

    pemilihs = db.query(Pemilihs).all()

    for pemilih in pemilihs:
        print(pemilih.id)

    def format_status(status):
        if status is True:
            return 'Aktif'
        elif status is False:
            return 'Tidak Aktif'
        else:
            return 'Belum dikonfirmasi'

    TABLE_DATA = ((str(idx+1), f"training/{pemilih.id}.1", pemilih.nama, pemilih.nik, pemilih.username, pemilih.alamat, format_status(pemilih.status))
                  for idx, pemilih in enumerate(pemilihs))

    pdf.set_font("Times", size=10)
    line_height_header = pdf.font_size * 2
    line_height = pdf.font_size * 8
    col_width = pdf.epw / 7

    TABLE_COL_WIDTH = [col_width + ((col_width-10) / 6) for i in range(6)]

    TABLE_COL_WIDTH.insert(0, 10.0)
    

    render_table_header(pdf, TABLE_COL_NAMES,TABLE_COL_WIDTH, line_height_header)

    for row in TABLE_DATA:
        for idx, data in enumerate(row):
            if idx == 1:
                pdf.cell(TABLE_COL_WIDTH[idx], line_height,  border=1)
                y = pdf.get_y()
                x = pdf.get_x()
                
                try:
                    pdf.image(
                    f"https://res.cloudinary.com/{cloud_name}/image/upload/q_auto:low,w_100,h_100/{data}", h=20, w=20, x=35, y=y+(line_height/6))
                    
                except:
                    pdf.image(
                    "./assets/users.jpeg", h=20, w=20, x=35, y=y+(line_height/6))

                pdf.set_y(y)
                pdf.set_x(x)
                
            else:
                pdf.cell(TABLE_COL_WIDTH[idx], line_height,
                     data, border=1, align="C")
        pdf.ln(line_height)

    pdf.output(path)
    return path


def cetak_daftar_vote(db: Session):
    path = 'assets/daftar_vote.pdf'
    pdf = FPDF()
    pdf.add_page(orientation="landscape", format="LEGAL")

    TABLE_COL_NAMES = ("NO", "NAMA VOTE", "KETERANGAN", "TANGGAL MULAI",
                       "TANGGAL SELESAI", "JUMLAH KANDIDAT", "JUMLAH PEMILIH", "STATUS")

    daftar_votes = db.query(DaftarVotes).all()

    def format_tanggal(tanggal: date, jam: time):
        return datetime.combine(tanggal, jam).strftime("%m/%d/%Y, %H:%M:%S")

    def format_status(tanggal_mulai: datetime, tanggal_selesai: datetime):
        now = datetime.now()

        if now < tanggal_mulai:
            return 'Belum Aktif'
        elif tanggal_mulai < now < tanggal_selesai:
            return 'Aktif'
        elif now > tanggal_selesai:
            return 'Selesai'

    TABLE_DATA = ((str(idx+1), daftar_vote.nama, daftar_vote.keterangan, format_tanggal(daftar_vote.tanggal_mulai, daftar_vote.jam_mulai), format_tanggal(daftar_vote.tanggal_selesai, daftar_vote.jam_selesai), str(len(daftar_vote.list_kandidat)), str(len(daftar_vote.list_pemilih)), format_status(datetime.combine(daftar_vote.tanggal_mulai, daftar_vote.jam_mulai), datetime.combine(daftar_vote.tanggal_selesai, daftar_vote.jam_selesai)))
                  for idx, daftar_vote in enumerate(daftar_votes))

    pdf.set_font("Times", size=12)
    line_height = pdf.font_size * 2
    col_width = pdf.epw / len(TABLE_COL_NAMES)

    TABLE_COL_WIDTH = [col_width + (-(10 - col_width) / (len(TABLE_COL_NAMES)-1))
                       for i in range(len(TABLE_COL_NAMES)-1)]

    TABLE_COL_WIDTH.insert(0, 10.0)


    render_table_header(pdf, TABLE_COL_NAMES,TABLE_COL_WIDTH, line_height)

    for row in TABLE_DATA:
        if pdf.will_page_break(line_height):
            render_table_header(pdf, TABLE_COL_NAMES,TABLE_COL_WIDTH, line_height)
        y = pdf.get_y()
        lh = max([(pdf.get_string_width(data)/TABLE_COL_WIDTH[idx])*8 for idx, data in enumerate(row)]);
            
        for idx, data in enumerate(row):
            pdf.set_xy(pdf.get_x(), y)
            pdf.multi_cell(TABLE_COL_WIDTH[idx], lh,
                     data, border=1, align="C", max_line_height=6,ln=0 if len(row) != idx+1 else 1)
        # pdf.ln(line_height)

    pdf.output(path)
    return path

def render_table_header(pdf, TABLE_COL_NAMES,TABLE_COL_WIDTH, line_height):
        pdf.set_font(style="B")
        for idx, col_name in enumerate(TABLE_COL_NAMES):
            pdf.cell(TABLE_COL_WIDTH[idx], line_height, col_name,
                     border=1, align='C')
        pdf.ln(line_height)
        pdf.set_font(style="")