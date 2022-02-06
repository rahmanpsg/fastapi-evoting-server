from datetime import datetime, date, time
import os
from fpdf import FPDF
from sqlalchemy.orm import Session
from models.daftar_vote import DaftarVotes

from models.kandidat import Kandidats
from models.pemilih import Pemilihs


def cetak_kandidat(db: Session):
    path = 'assets/kandidat.pdf'
    cloud_name = os.getenv('CLOUD_NAME')
    pdf = FPDF()
    pdf.add_page()

    TABLE_COL_NAMES = ("No", "Foto", "Nama", "Keterangan")

    kandidats = db.query(Kandidats).all()

    TABLE_DATA = ((str(idx+1), kandidat.foto, kandidat.nama, kandidat.keterangan)
                  for idx, kandidat in enumerate(kandidats))

    pdf.set_font("Times", size=16)
    line_height = pdf.font_size * 4
    col_width = pdf.epw / 4

    def render_table_header():
        pdf.set_font(style="B")
        for col_name in TABLE_COL_NAMES:
            pdf.cell(col_width, line_height - 10, col_name,
                     border=1, align='C')
        pdf.ln(line_height - 10)
        pdf.set_font(style="")

    render_table_header()

    for row in TABLE_DATA:
        if pdf.will_page_break(line_height):
            render_table_header()
        for idx, data in enumerate(row):
            if idx == 1:
                pdf.cell(col_width, line_height,  border=1)
                y = pdf.get_y()
                x = pdf.get_x()
                pdf.image(
                    f"https://res.cloudinary.com/{cloud_name}/image/upload/{data}", h=20, w=20, x=70, y=y+1.3)
                pdf.set_y(y)
                pdf.set_x(x)
            else:
                pdf.cell(col_width, line_height, data, border=1, align="C")
        pdf.ln(line_height)

    pdf.output(path)
    return path


def cetak_pemilih(db: Session):
    path = 'assets/pemilih.pdf'
    pdf = FPDF()
    pdf.add_page()

    TABLE_COL_NAMES = ("NO", "NAMA", "NIK", "USERNAME", "ALAMAT", "STATUS")

    pemilihs = db.query(Pemilihs).all()

    def format_status(status):
        if status is True:
            return 'Aktif'
        elif status is False:
            return 'Tidak Aktif'
        else:
            return 'Belum dikonfirmasi'

    TABLE_DATA = ((str(idx+1), kandidat.nama, kandidat.nik, kandidat.username, kandidat.alamat, format_status(kandidat.status))
                  for idx, kandidat in enumerate(pemilihs))

    pdf.set_font("Times", size=12)
    line_height = pdf.font_size * 2
    col_width = pdf.epw / 6

    TABLE_COL_WIDTH = [col_width + ((col_width-10) / 5) for i in range(5)]

    TABLE_COL_WIDTH.insert(0, 10.0)

    def render_table_header():
        pdf.set_font(style="B")
        for idx, col_name in enumerate(TABLE_COL_NAMES):
            pdf.cell(TABLE_COL_WIDTH[idx], line_height, col_name,
                     border=1, align='C')
        pdf.ln(line_height)
        pdf.set_font(style="")

    render_table_header()

    for row in TABLE_DATA:
        if pdf.will_page_break(line_height):
            render_table_header()
        for idx, data in enumerate(row):
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

    

    

    def render_table_header():
        pdf.set_font(style="B")
        for idx, col_name in enumerate(TABLE_COL_NAMES):
            pdf.cell(TABLE_COL_WIDTH[idx], line_height, col_name,
                     border=1, align='C')
        pdf.ln(line_height)
        pdf.set_font(style="")

    render_table_header()

    for row in TABLE_DATA:
        if pdf.will_page_break(line_height):
            render_table_header()

        for idx, data in enumerate(row):
            pdf.cell(TABLE_COL_WIDTH[idx], line_height,
                     data, border=1, align="C")
        pdf.ln(line_height)

    pdf.output(path)
    return path
