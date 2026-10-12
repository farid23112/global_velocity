# M7 — Kecepatan Koordinat Global (ROS 2)

Node ROS 2 berbasis Python yang membaca data dari topic `/joint_states`, menghitung estimasi kecepatan robot beroda diferensial (*differential drive*), dan menampilkan komponen kecepatan pada sumbu X dan Y koordinat global melalui terminal.

## Hasil Keluaran

Node menampilkan beberapa nilai berikut:

- `Vx`: Komponen estimasi kecepatan pada sumbu X global (m/s).
- `Vy`: Komponen estimasi kecepatan pada sumbu Y global (m/s).
- `Omega`: Kecepatan sudut robot (rad/s).
- `Theta`: Estimasi sudut orientasi robot (derajat).

## Persyaratan

Perangkat lunak dan komponen yang diperlukan:

- ROS 2 dengan pustaka `rclpy`.
- Paket pesan ROS 2 `sensor_msgs`.
- Robot atau simulasi yang menerbitkan data kecepatan putaran roda melalui topic `/joint_states`.

## Konfigurasi Nama Joint Robot

Parameter bawaan pada program adalah sebagai berikut:

- Radius roda: `0.10 m`.
- Jarak antara roda kiri dan kanan: `0.45 m`.
- Nama joint roda kiri: `base_left_wheel_joint`.
- Nama joint roda kanan: `base_right_wheel_joint`.

Periksa nama joint yang digunakan oleh model robot melalui perintah berikut:

```bash
ros2 topic echo /joint_states
```

Jika nama joint pada model robot berbeda dari parameter bawaan, sesuaikan parameter saat menjalankan node.

## Kompilasi Program (Build)

Letakkan folder package `simple_mover` di dalam direktori `~/ros2_ws/src/`, kemudian jalankan perintah berikut:

```bash
cd ~/ros2_ws
colcon build --packages-select simple_mover
source install/setup.bash
```

## Menjalankan Program

Pastikan simulasi robot sudah berjalan. Kemudian, jalankan node menggunakan perintah berikut:

```bash
ros2 run simple_mover global_velocity
```


## Menyesuaikan Parameter Robot

Jika nama joint atau dimensi robot berbeda dari konfigurasi standar, parameter dapat disesuaikan saat menjalankan node.

### Contoh Perintah

```bash
ros2 run simple_mover global_velocity --ros-args \
  -p left_joint:=left_wheel_joint \
  -p right_joint:=right_wheel_joint \
  -p wheel_radius:=0.10 \
  -p wheel_separation:=0.45
```

### Penjelasan Parameter

| Parameter | Deskripsi | Contoh Nilai |
|---|---|---|
| `left_joint` | Nama joint roda kiri robot | `left_wheel_joint` |
| `right_joint` | Nama joint roda kanan robot | `right_wheel_joint` |
| `wheel_radius` | Radius roda dalam meter | `0.10` |
| `wheel_separation` | Jarak antara roda kiri dan kanan dalam meter | `0.45` |

**Catatan:** Sesuaikan nama joint, radius roda, dan jarak antarroda dengan konfigurasi robot yang digunakan.

Untuk memeriksa nama joint yang benar, jalankan perintah berikut saat simulasi aktif:

```bash
ros2 topic echo /joint_states
```


## ⚙️ Prinsip Kerja Program

Program menggunakan data kecepatan sudut roda kiri dan kanan untuk menghitung kecepatan linear serta kecepatan sudut robot.

### 📌 Keterangan Variabel

- **r** = radius roda (meter).
- **L** = jarak antara roda kiri dan kanan (meter).
- **ωR** = kecepatan sudut roda kanan (rad/s).
- **ωL** = kecepatan sudut roda kiri (rad/s).
- **θ** = estimasi orientasi robot terhadap sumbu X global (radian).

### 1. Kecepatan Linear Robot

Kecepatan linear robot dihitung berdasarkan rata-rata kecepatan kedua roda:

$$
v = \frac{r(\omega_R + \omega_L)}{2}
$$

### 2. Kecepatan Sudut Robot

Kecepatan sudut robot dihitung berdasarkan selisih kecepatan roda kanan dan kiri:

$$
\omega = \frac{r(\omega_R - \omega_L)}{L}
$$

### 3. Transformasi ke Koordinat Global

Kecepatan linear robot ditransformasikan ke koordinat global berdasarkan orientasi robot:

$$
V_x = v\cos(\theta)
$$

$$
V_y = v\sin(\theta)
$$

Keterangan:

- **Vₓ** = komponen kecepatan pada sumbu X global (m/s).
- **Vᵧ** = komponen kecepatan pada sumbu Y global (m/s).

### 4. Estimasi Orientasi Robot

Orientasi robot dihitung dengan mengintegrasikan kecepatan sudut terhadap waktu, dimulai dari orientasi awal nol radian.

Metode ini disebut *dead reckoning*, yaitu estimasi gerakan robot berdasarkan data pergerakan roda. Metode ini dapat mengalami penyimpangan (*drift*) seiring waktu sehingga tidak memberikan pengukuran posisi global absolut.

Untuk memperoleh estimasi kecepatan global yang lebih akurat, data odometri atau transformasi TF dari simulator dapat digunakan apabila tersedia dan terkonfigurasi dengan benar.


## Pemecahan Masalah (Troubleshooting)

Jika node tidak menampilkan nilai kecepatan, periksa beberapa hal berikut:

1. Pastikan topic `/joint_states` menerbitkan data menggunakan perintah:

   ```bash
   ros2 topic echo /joint_states
   ```

2. Pastikan nama joint roda kiri dan kanan pada program sesuai dengan nama yang diterbitkan oleh topic.

3. Pastikan pesan `/joint_states` memiliki data kecepatan roda pada field `velocity`.

4. Pastikan timestamp pada pesan valid dan terus bertambah selama simulasi berjalan.

5. Periksa kembali nilai radius roda dan jarak antarroda agar sesuai dengan model robot yang digunakan.

## Kesimpulan

Node `global_velocity` digunakan untuk menghitung dan menampilkan estimasi komponen kecepatan robot pada koordinat global X dan Y melalui terminal. Program ini memanfaatkan data kecepatan putaran roda dari ROS 2 dan dapat diuji menggunakan simulasi robot di Gazebo.
