from manim import *
import numpy as np

class EulerEpicycles(MovingCameraScene):
    def construct(self):
        # ==========================================
        # 全局配置：初始化支持中文的 LaTeX 模板
        # ==========================================
        ctex = TexTemplate()
        ctex.add_to_preamble(r"\usepackage[UTF8]{ctex}")

        # ==========================================
        # 第一段画面：标题与坐标系的引入
        # ==========================================
        
        formula = MathTex(r"Z(\theta) = e^{i\theta} + e^{i", r"3.14", r"\theta}").scale(0.8)
        formula.set_color(PINK)
        formula[1].set_color(TEAL)
        
        theta_label = MathTex(r"\theta = ").scale(0.8)
        theta_num = DecimalNumber(0, num_decimal_places=2, color=YELLOW).scale(0.8)
        theta_group = VGroup(theta_label, theta_num).arrange(RIGHT)
        
        header = VGroup(formula, theta_group).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.1)
        
        self.play(Write(header))
        self.wait(1)

        plane = ComplexPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6.5,
            y_length=6.5,
            background_line_style={"stroke_color": GREY, "stroke_opacity": 0.4}
        ).shift(DOWN * 0.5)
        # 隐藏坐标系：移除 Create(plane)，但保留 plane 对象用于提供 c2p 坐标转换支持

        # ==========================================
        # 第二段画面：核心绘图与动态追踪
        # ==========================================
        # 将起点改至第三象限 (theta = 3.5)
        theta_tracker = ValueTracker(3.5)
        theta_num.add_updater(lambda m: m.set_value(theta_tracker.get_value()))

        # 动态控制线宽与点大小的 Tracker（用于放大镜头时变细线条）
        line_width = ValueTracker(2.0)
        dot_radius = ValueTracker(0.035)
        path_width = ValueTracker(1.5)

        # 辅助函数：计算向量端点在复平面中的坐标
        def get_origin():
            return plane.c2p(0, 0)

        def get_A():
            theta = theta_tracker.get_value()
            # 放大向量长度 (2倍) 
            return plane.c2p(2 * np.cos(theta), 2 * np.sin(theta))

        def get_B():
            theta = theta_tracker.get_value()
            # e^{i\theta} + e^{i3.14\theta} 并同步放大
            x = 2 * np.cos(theta) + 2 * np.cos(3.14 * theta)
            y = 2 * np.sin(theta) + 2 * np.sin(3.14 * theta)
            return plane.c2p(x, y)

        # 1. 绘制两段线段 (Line)
        line_A = always_redraw(lambda: Line(
            start=get_origin(), end=get_A(), color=BLUE, stroke_width=line_width.get_value()
        ))

        line_B = always_redraw(lambda: Line(
            start=get_A(), end=get_B(), color=GREEN, stroke_width=line_width.get_value()
        ))

        # 2. 绘制彩色圆点 (Dot)
        dot_A = always_redraw(lambda: Dot(get_A(), color=RED, radius=dot_radius.get_value()).set_z_index(3))
        dot_B = always_redraw(lambda: Dot(get_B(), color=BLUE, radius=dot_radius.get_value()).set_z_index(3))

        # 3. 追踪轨迹 (极致性能与绝对零误差版)
        # 摒弃 pointwise_become_partial 带来的弧长比例偏差
        # 采用底层 Numpy 矢量化直接生成当前 theta 进度的点集，渲染快且完美吸附！
        FINAL_THETA = 3.5 + 100 * PI
        path = VMobject(color=WHITE).set_z_index(2)
        
        origin_pt = plane.get_origin()
        x_unit = plane.get_x_unit_size()
        y_unit = plane.get_y_unit_size()

        def update_path(mob):
            current_theta = theta_tracker.get_value()
            if current_theta <= 3.501:
                t_vals = np.array([3.5, current_theta])
            else:
                # 步长 0.01 极其精细，即使镜头放大 10 倍也看不出折线
                t_vals = np.arange(3.5, current_theta, 0.01)
                if t_vals[-1] != current_theta:
                    t_vals = np.append(t_vals, current_theta)
            
            x_vals = 2 * np.cos(t_vals) + 2 * np.cos(3.14 * t_vals)
            y_vals = 2 * np.sin(t_vals) + 2 * np.sin(3.14 * t_vals)
            
            points = np.zeros((len(t_vals), 3))
            points[:, 0] = origin_pt[0] + x_vals * x_unit
            points[:, 1] = origin_pt[1] + y_vals * y_unit
            points[:, 2] = origin_pt[2]
            
            # 使用 set_points_as_corners 直接绘制多边形顶点，性能极佳，且强行保证终端位置严丝合缝
            mob.set_points_as_corners(points)
            mob.set_stroke(width=path_width.get_value())

        path.add_updater(update_path)

        # 3.5 真正的彗星发光拖尾 (利用数组切片实现完美渐变)
        num_trail_segments = 15
        trail_length = 1.2
        trail_glows = VGroup(*[VMobject(color=LIGHT_GREY).set_z_index(1) for _ in range(num_trail_segments)])
        
        def update_trail(mob):
            current_theta = theta_tracker.get_value()
            start_theta = max(3.5, current_theta - trail_length)
            
            if current_theta <= 3.501:
                for layer in mob:
                    layer.set_points_as_corners([origin_pt, origin_pt]).set_stroke(opacity=0)
                return
                
            t_vals = np.arange(start_theta, current_theta, 0.01)
            if t_vals[-1] != current_theta:
                t_vals = np.append(t_vals, current_theta)
                
            if len(t_vals) < 2:
                for layer in mob:
                    layer.set_points_as_corners([origin_pt, origin_pt]).set_stroke(opacity=0)
                return
                
            x_vals = 2 * np.cos(t_vals) + 2 * np.cos(3.14 * t_vals)
            y_vals = 2 * np.sin(t_vals) + 2 * np.sin(3.14 * t_vals)
            
            pts = np.zeros((len(t_vals), 3))
            pts[:, 0] = origin_pt[0] + x_vals * x_unit
            pts[:, 1] = origin_pt[1] + y_vals * y_unit
            pts[:, 2] = origin_pt[2]
            
            splits = np.array_split(pts, num_trail_segments)
            base_width = path_width.get_value()
            fallback_pts = np.array([pts[0], pts[0]])
            
            for i, layer in enumerate(mob):
                alpha = (i + 1) / num_trail_segments
                current_opacity = 0.7 * alpha
                
                if len(splits[i]) > 0:
                    if i < num_trail_segments - 1 and len(splits[i+1]) > 0:
                        seg_pts = np.vstack((splits[i], splits[i+1][0])) # 缝合段与段的断层
                    else:
                        seg_pts = splits[i]
                        
                    if len(seg_pts) >= 2:
                        layer.set_points_as_corners(seg_pts)
                    else:
                        layer.set_points_as_corners(fallback_pts)
                        current_opacity = 0
                else:
                    layer.set_points_as_corners(fallback_pts)
                    current_opacity = 0
                    
                # 越靠近头部，宽度拉伸为白线的 3.5 倍，制造晕开的光效
                layer.set_stroke(width=base_width * 3.5 * alpha, opacity=current_opacity)

        trail_glows.add_updater(update_trail)

        # 4. 精准起始点：直接使用 t=3.5 时的绝对数学坐标
        start_x = 2 * np.cos(3.5) + 2 * np.cos(3.14 * 3.5)
        start_y = 2 * np.sin(3.5) + 2 * np.sin(3.14 * 3.5)
        start_dot = always_redraw(lambda: Dot(plane.c2p(start_x, start_y), color=PURPLE_A, radius=dot_radius.get_value()).set_z_index(3))
        
        self.add(start_dot, trail_glows, line_A, line_B, dot_A, dot_B, path)
        
        # --- 动画节奏与运镜控制 ---
        # 1. 快速绘制到快对接的前夕 (经数学计算，第一次精确接近起点在 theta ≈ 47.48)
        self.play(theta_tracker.animate.set_value(46.5), run_time=6, rate_func=linear)
        
        # 2. 突然减慢，缓慢绘制到极度接近起点的位置 (47.45) 并停下
        self.play(theta_tracker.animate.set_value(47.45), run_time=3, rate_func=linear)
        self.wait(0.5)
        
        # 3. 画面逐渐放大，以当前追踪点为中心，同时同步变细所有的线段和圆点
        self.play(
            self.camera.frame.animate.scale(0.3).move_to(dot_B.get_center()),
            path_width.animate.set_value(0.5),  # 轨迹线变细
            line_width.animate.set_value(0.6),  # 转盘线段变细
            dot_radius.animate.set_value(0.012),# 圆点等比例缩小
            run_time=2
        )
        
        # 让摄像机在接下来的绘制中死死锁定并跟随追踪点
        self.camera.frame.add_updater(lambda m: m.move_to(dot_B.get_center()))
        
        # 4. 保持镜头跟随，继续慢速绘制，穿过起点完成微观视角的完美对接
        self.play(theta_tracker.animate.set_value(49.0), run_time=4, rate_func=linear)
        
        # 5. 停止镜头跟随，并让画面缩放和位置恢复，同时恢复所有线宽与大小
        self.camera.frame.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(1/0.3).move_to(ORIGIN),
            path_width.animate.set_value(1.5),
            line_width.animate.set_value(2.0),
            dot_radius.animate.set_value(0.035),
            run_time=2
        )
        
        # 6. 恢复正常速度，向着第二次接近点冲刺 (经严格计算，k=43 时，theta = 3.5 + 86π ≈ 273.68)
        self.play(theta_tracker.animate.set_value(272.5), run_time=8, rate_func=linear)
        
        # 7. 第二次接近前夕，减速并停下
        self.play(theta_tracker.animate.set_value(273.60), run_time=3, rate_func=linear)
        self.wait(0.5)
        
        # 8. 再次放大，以更宏观的微观视角观察第二次对接 (这次偏离同样只有大约 7.2 度)
        self.play(
            self.camera.frame.animate.scale(0.2).move_to(dot_B.get_center()),
            path_width.animate.set_value(0.3),
            line_width.animate.set_value(0.4),
            dot_radius.animate.set_value(0.008),
            run_time=2
        )
        
        self.camera.frame.add_updater(lambda m: m.move_to(dot_B.get_center()))
        
        # 9. 慢速穿过第二次对接点 (穿过 273.68)
        self.play(theta_tracker.animate.set_value(275.0), run_time=4, rate_func=linear)
        
        # 10. 停止跟随，恢复视角
        self.camera.frame.clear_updaters()
        self.play(
            self.camera.frame.animate.scale(1/0.2).move_to(ORIGIN),
            path_width.animate.set_value(1.5),
            line_width.animate.set_value(2.0),
            dot_radius.animate.set_value(0.035),
            run_time=2
        )

        # 11. 终极冲刺！向着真正的完全闭合点前进 (经计算，完全闭合在 theta = 3.5 + 100π ≈ 317.6593)
        self.play(theta_tracker.animate.set_value(316.5), run_time=6, rate_func=linear)
        
        # 12. 终极对接前夕减速停下
        self.play(theta_tracker.animate.set_value(317.60), run_time=3, rate_func=linear)
        self.wait(0.5)

        # 13. 最后一次极致放大！(因为这次是真正的 0 误差对接，我们放到最大)
        self.play(
            self.camera.frame.animate.scale(0.1).move_to(dot_B.get_center()),
            path_width.animate.set_value(0.15),
            line_width.animate.set_value(0.2),
            dot_radius.animate.set_value(0.004),
            run_time=2
        )
        self.camera.frame.add_updater(lambda m: m.move_to(dot_B.get_center()))

        # 14. 见证奇迹的时刻，严格停在绝对的数学闭合点
        self.play(theta_tracker.animate.set_value(FINAL_THETA), run_time=4, rate_func=linear)

        # ==========================================
        # 第三段画面：突出最终轨迹并落幕
        # ==========================================
        
        # 1. 停止视角跟随（保留路径更新器，确保在恢复视角时线条能跟着变粗）
        self.camera.frame.clear_updaters()

        # 15. 完美对接后恢复视角，准备最终落幕
        self.play(
            self.camera.frame.animate.scale(1/0.1).move_to(ORIGIN),
            path_width.animate.set_value(2.0), 
            line_width.animate.set_value(2.0),
            dot_radius.animate.set_value(0.035),
            run_time=2
        )
        
        # 在最终缩放落幕前，彻底关闭更新器，解除轨迹与坐标系的数学绑定，让其成为独立的静态图形
        path.clear_updaters()
        trail_glows.clear_updaters()

        # 16. 隐去其他辅助元素，保留最终闭合的纯粹轨迹
        self.play(
            FadeOut(start_dot), FadeOut(line_A), FadeOut(line_B), 
            FadeOut(dot_A), FadeOut(dot_B), FadeOut(header), FadeOut(trail_glows),
            run_time=1.5
        )
        
        self.play(path.animate.scale(1.3), run_time=3)
        self.wait(2)
        self.play(FadeOut(path))