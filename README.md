# 🏀 AI-Powered Basketball Game Analyzer (v1)

> **Personalized & Complete Version of an Academic Project**  
> 🔁 Rewritten, restructured, and integrated from scratch by Hana FEKI

---

## 📘 Project Context

This project was initially part of a **group academic project at ENSTA Paris** during the 2024–2025 academic year. We were a team of **10 students**, split into **5 subgroups**, each responsible for a specific part of the system (e.g., detection, tracking, analytics, etc.).

Due to tight academic deadlines and the distributed nature of the work, the project:
- Was not fully completed
- Had parts that remained unintegrated
- Lacked a unified and polished implementation

---

## ❤️ Why This Version Exists (v1)

As I was **deeply passionate** about the topic, I decided to **rebuild the entire system from A to Z** by myself:
- Rewriting every component
- Organizing everything into a single, consistent pipeline
- Fixing bugs and improving the original implementation
- Adding missing features and enhancements

> 📁 The original version (v0) is available here: https://github.com/HanaFEKI/AI_BasketBall_Analysis_v0  
> ✅ This repository is the **personalized, cleaned-up, and extended version (v1)**.

---

## 🎥 Demo Video

👉 **Watch the full demonstration of this system here:**  
[🔗 Insert your video link]

---

## ⚙️ How It Works

This system analyzes basketball games from video using computer vision and AI:

1. **🎯 Object Detection (YOLO)**  
   Detect players and the basketball in each frame.

2. **🧭 Object Tracking (ByteTrack)**  
   Track players and the ball across video frames.

3. **🎨 Team Classification (Zero-Shot with Hugging Face)**  
   Automatically assign players to teams based on jersey colors using a zero-shot image classifier.

4. **📍 Court Keypoint Detection**  
   Detect basketball court landmarks using a keypoint detection model trained on a labeled dataset.

5. **🔄 Perspective Transformation**  
   Convert broadcast view into a **top-down tactical map** using homography and real-world court dimensions.

6. **📊 Analytics**  
   - Count **passes** and **interceptions**  
   - Compute **ball possession** percentage  
   - Calculate **player speed** and **distance covered** (in meters)

---

## 🗂️ Project Structure

