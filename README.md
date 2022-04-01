# Fifteen Puzzle Solver

Merupakan project menggunakan bahasa pemrograman Python untuk membuat algoritma _15-Puzzle solver_ menggunakan strategi _branch and bound_. Proyek ini dibuat untuk pemenuhan tugas kecil 3 IF2211 Strategi Algoritma.

## Daftar Isi

- [Deskripsi Singkat](#deskripsi-singkat)
- [Requirement](#requirement)
- [Setup](#setup)
- [Usage](#usage)
- [Author](#author)

## Deskripsi Singkat
_Fifteen Puzzle_ merupakan permainan menyusun puzzle 15 block dalam 16 buah tile, dimana pemain hanya boleh untuk menggeser block yang tersedia melalui tile kosong. Pustaka ini merupakan program implementasi penyelesaian puzzle tersebut menggunakan strategi _branch and bound_. Pustaka ini juga dilengkapi visualisasi yang dapat digunakan dalam menampilkan pergeseran secara interaktif.

## Requirement
1. Python >= 3.8 + tkinter (optional, untuk GUI)

## Setup
> Program ini memerlukan tkinter untuk menjalankan GUI. Install tkinter [disini](https://tkdocs.com/tutorial/install.html).
1. **[RECOMMENDED]** Gunakan virtual environment Python baru.
2. Change directory ke folder project ini.
3. Install package dengan command berikut:
    ```
    pip install .
    ```
    
    > Untuk pengembangan, jalankan `pip install -e .` sehingga package terinstall dalam edit mode.

## Usage
### A. Library
Package dapat digunakan sebagai module python yang bisa diimport oleh program lain.
Terdapat tiga kelas utama, yakni `Visualizer`, `Solver`, dan `Puzzle`.

1. `Visualizer` dapat digunakan untuk menampilkan UI interaktif menggunakan implementasi dari solver.

2. `Solver` dapat digunakan untuk menyelesaikan persoalan 15-puzzle.

3. `Puzzle` digunakan untuk internal solver dalam menampung data/node yang perlu untuk solver.

Untuk dokumentasi lebih lanjut, lihat docstring dari masing-masing kelas/fungsi yang akan digunakan.

Beberapa sample program yang dapat digunakan sebagai referensi:
1. Menyelesaikan instansi persoalan fifteen puzzle dari string.
    ```py
    from FifteenPuzzleSolver.solver import Solver
    print(Solver("3 1 2 4\n- 5 7 8\n10 6 11 12\n9 13 14 15"))
    ```
2. Menyelesaikan instansi persoalan fifteen puzzle dari file.
    ```py
    from FifteenPuzzleSolver.solver import Solver
    with open("test/test.txt", "r") as f:
        print(Solver(f.read()))
    ```
3. Menampilkan GUI dari solver.
    ```py
    from FifteenPuzzleSolver.Visualizer import Visualizer
    Visualizer()
    ```
### B. Driver / Main Program
Package ini juga dilengkapi dengan driver program utama yang dapat dijalankan pada command line. Untuk melihat argumen lebih lengkap, jalankan command berikut:
```sh
python -m FifteenPuzzleSolver -h
```
Berikut argumen lengkap untuk menjalankan `python -m FifteenPuzzleSolver`:
```
usage: __main__.py [-h] [-f FILE] [-g] [-i]

Main driver of Fifteen Puzzle Solver. It will generate a solution path for the problem instantiation. You can supply manually the initial state of the puzzle to show in GUI by specify -i/--input and -g/--gui.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  input file path.
  -g, --gui             show GUI visualizer.
  -i, --input           get puzzle from input.
```

Beberapa contoh command yang dapat dieksekusi:
1. Menjalankan solver untuk input berupa file di CLI.
    ```sh
    python -m FifteenPuzzleSolver -f test/berhasil1.txt
    ```
2. Menjalankan solver untuk input berupa keyboard di CLI.
    ```sh
    python -m FifteenPuzzleSolver
    ```
3. Menjalankan solver untuk input berupa file di GUI.
    ```sh
    python -m FifteenPuzzleSolver -f test/berhasil1.txt -g
    ```
4. Menjalankan solver untuk input berupa keyboard di GUI.
    ```sh
    python -m FifteenPuzzleSolver -i -g
    ```
5. Tampilkan GUI solver saja.
    ```sh
    python -m FifteenPuzzleSolver -g 
    ```

## Author

**Amar Fadil** [13520103]

Halo, saya Amar Fadil, mahasiswa IF dengan NIM 13520103, adalah seorang software engineer yang suka ngoprek grafika komputer, computer security, dan competitive programming (maybe). Berkuliah dalam program studi/jurusan Teknik Informatika (IF) pada fakultas Sekolah Teknik Elektro dan Informatika (STEI) di Institut Teknologi Bandung (ITB), saya bercita-cita untuk mengembangkan industri digital kreatif di Indonesia :D
