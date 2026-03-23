from manim import *
import numpy as np
import random

class AmazingMathEquations(Scene):
    def construct(self):
        # 备选的浅色系颜色
        colors = [PURPLE_A, YELLOW_A, BLUE_A, GREEN_A, RED_A]

        # ==========================================
        # 第一段画面：居中写出文字，伴随逐渐放大的效果
        # ==========================================
        title = Text("那些令人惊艳的数学方程图像", color=WHITE)
        title.scale(0.7)  # 初始 70% 大小

        for char in title:
            char.set_opacity(0)

        time_tracker = ValueTracker(0)
        def reveal_chars(mob):
            progress = time_tracker.get_value()
            num_chars = len(mob)
            if num_chars == 0:
                return
            for i, char in enumerate(mob):
                start_p = i / num_chars * 0.8
                char.set_opacity(min(max((progress - start_p) / 0.2, 0), 1))

        title.add_updater(reveal_chars)

        self.play(
            title.animate.scale(1/0.7),
            time_tracker.animate.set_value(1),
            run_time=3
        )
        title.remove_updater(reveal_chars)
        self.wait(1)
        self.play(FadeOut(title))

        # ==========================================
        # 第二段画面：y = x^{2/3} + 0.9\sqrt{8 - x^2}\sin(k\pi x) - 1
        # ==========================================
        axes1 = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"color": GREY},
        )

        k_tracker1 = ValueTracker(0)

        eq1_left = MathTex(r"y = x^{\frac{2}{3}} + 0.9\sqrt{8 - x^2}\sin(")
        k_num1 = DecimalNumber(0, num_decimal_places=2, color=YELLOW_A)
        eq1_right = MathTex(r"\pi x) - 1")
        
        eq1 = VGroup(eq1_left, k_num1, eq1_right).arrange(RIGHT, buff=0.05).to_edge(UP).set_z_index(2)
        
        eq1.add_updater(lambda m: m.arrange(RIGHT, buff=0.05).to_edge(UP))
        k_num1.add_updater(lambda m: m.set_value(k_tracker1.get_value()))

        def get_heart_curve():
            k_val = k_tracker1.get_value()
            # 使用 max 防止浮点误差导致的复数域计算
            return axes1.plot(
                lambda x: np.cbrt(x**2) + 0.9 * np.sqrt(max(8 - x**2, 0)) * np.sin(k_val * PI * x) - 1,
                x_range=[-np.sqrt(8), np.sqrt(8)],
                color=RED_A
            )

        curve1 = always_redraw(get_heart_curve)

        self.play(Write(eq1), Create(axes1))
        self.play(Create(curve1))
        
        # k 从 0 增加到 9.99，然后再减小到 0
        self.play(k_tracker1.animate.set_value(9.99), run_time=5, rate_func=linear)
        self.wait(0.5)
        self.play(k_tracker1.animate.set_value(0), run_time=5, rate_func=linear)
        
        self.play(FadeOut(eq1), FadeOut(curve1), FadeOut(axes1))

        # ==========================================
        # 第三段画面：一系列直接切换的方程图像
        # ==========================================
        axes2 = Axes(
            x_range=[-8, 8, 1],
            y_range=[-4.5, 4.5, 1],
            x_length=config.frame_width,
            y_length=config.frame_height,
            axis_config={"color": GREY},
        )
        self.play(Create(axes2))

        equations_data = [
            {"tex": r"\sin(x^2) = \sin(y^2)", "type": "implicit", "func": lambda x, y: np.sin(x**2) - np.sin(y**2)},
            {"tex": r"\sin(x^2 + y^2) = \cos(xy)", "type": "implicit", "func": lambda x, y: np.sin(x**2 + y**2) - np.cos(x*y)},
            {"tex": r"\sin(xy) + \cos(xy) = 1", "type": "implicit", "func": lambda x, y: np.sin(x*y) + np.cos(x*y) - 1},
            # 为避免分母为0时的断崖式报错，等式两边同乘 \cos(xy)
            {"tex": r"\frac{1}{\cos(xy)} + \cos(x^2 + y^2) = 1", "type": "implicit", "func": lambda x, y: 1 + np.cos(x**2 + y**2)*np.cos(x*y) - np.cos(x*y)},
            {"tex": r"2^{\sin(3x) + \cos(3y)} = \sin 2", "type": "implicit", "func": lambda x, y: 2**(np.sin(3*x) + np.cos(3*y)) - np.sin(2)},
            {"tex": r"\sin(\cos(3y)) = \cos(\sin(3x))", "type": "implicit", "func": lambda x, y: np.sin(np.cos(3*y)) - np.cos(np.sin(3*x))},
            # 极坐标转换为参数方程进行绘制
            {"tex": r"r = 5\cos\theta - \cos(5\theta)", "type": "parametric", "t_range": [0, 2*PI], "func": lambda t: np.array([(5*np.cos(t) - np.cos(5*t)) * np.cos(t), (5*np.cos(t) - np.cos(5*t)) * np.sin(t), 0])},
            {"tex": r"(x^2 + y^2)^2 + 18(x^2 + y^2) - 27 = 8(x^3 - 3xy^2)", "type": "implicit", "func": lambda x, y: (x**2 + y**2)**2 + 18*(x**2 + y**2) - 27 - 8*(x**3 - 3*x*y**2)},
            {"tex": r"x^3 + y^3 = 5xy", "type": "implicit", "func": lambda x, y: x**3 + y**3 - 5*x*y},
            {"tex": r"x^{\frac{2}{3}} + y^{\frac{2}{3}} = 3^{\frac{2}{3}}", "type": "implicit", "func": lambda x, y: np.cbrt(x**2) + np.cbrt(y**2) - 3**(2/3)},
            # 使用 arctan2 稳定替代 x/y 防止除0错误
            {"tex": r"\cos\left(16\left(\arctan\frac{x}{y}\right)^4 + \arctan\left(\frac{y}{x+4}\right)\right) = 0", "type": "implicit", "func": lambda x, y: np.cos(16*(np.arctan2(x, y))**4 + np.arctan2(y, x+4))},
            {"tex": r"y\sin(8x) = x\sin(8y)", "type": "implicit", "func": lambda x, y: y*np.sin(8*x) - x*np.sin(8*y)},
        ]

        prev_eq, prev_curve = None, None

        for i, data in enumerate(equations_data):
            eq = MathTex(data["tex"]).to_edge(UP).set_z_index(2)
            eq.add_background_rectangle(color=BLACK, opacity=0.7, buff=0.1)
            
            c_color = random.choice(colors)
            if data["type"] == "implicit":
                curve = axes2.plot_implicit_curve(data["func"], color=c_color)
            else:
                curve = axes2.plot_parametric_curve(data["func"], t_range=data["t_range"], color=c_color)
            
            if i == 0:
                self.play(Write(eq), Create(curve), run_time=2)
            else:
                # 第一个之后，使用直接平滑替换（ReplacementTransform）已经画好的图像
                self.play(
                    ReplacementTransform(prev_eq, eq),
                    ReplacementTransform(prev_curve, curve),
                    run_time=1.5
                )
            self.wait(1.5)
            prev_eq, prev_curve = eq, curve

        self.play(FadeOut(prev_eq), FadeOut(prev_curve), FadeOut(axes2))

        # ==========================================
        # 第四段画面：\sin(x)\sin(y) = \cos(k)
        # ==========================================
        axes3 = Axes(
            x_range=[-8, 8, 1], y_range=[-4.5, 4.5, 1],
            x_length=config.frame_width, y_length=config.frame_height,
            axis_config={"color": GREY}
        )
        self.play(FadeIn(axes3))

        k_tracker2 = ValueTracker(0)
        
        eq4_left = MathTex(r"\sin(x)\sin(y) = \cos(")
        k_num2 = DecimalNumber(0, num_decimal_places=2, color=YELLOW_A)
        eq4_right = MathTex(")")
        
        eq4 = VGroup(eq4_left, k_num2, eq4_right).arrange(RIGHT, buff=0.05).to_edge(UP).set_z_index(2)
        
        eq4.add_updater(lambda m: m.arrange(RIGHT, buff=0.05).to_edge(UP))
        k_num2.add_updater(lambda m: m.set_value(k_tracker2.get_value()))

        color4 = random.choice(colors)
        curve4 = always_redraw(lambda: axes3.plot_implicit_curve(
            lambda x, y: np.sin(x)*np.sin(y) - np.cos(k_tracker2.get_value()), color=color4
        ))

        self.play(Write(eq4), Create(curve4))
        self.play(k_tracker2.animate.set_value(5.79), run_time=8, rate_func=linear)
        self.play(FadeOut(eq4), FadeOut(curve4), FadeOut(axes3))

        # ==========================================
        # 第五段画面：(x - k\cos y)^2 + (y - k\sin x)^2 = k
        # ==========================================
        axes4 = Axes(
            x_range=[-8, 8, 1], y_range=[-4.5, 4.5, 1],
            x_length=config.frame_width, y_length=config.frame_height,
            axis_config={"color": GREY}
        )
        self.play(FadeIn(axes4))

        k_tracker3 = ValueTracker(0)
        
        eq5_p1 = MathTex(r"(x - ")
        k_num3_1 = DecimalNumber(0, num_decimal_places=2, color=YELLOW_A)
        eq5_p2 = MathTex(r"\cos y)^2 + (y - ")
        k_num3_2 = DecimalNumber(0, num_decimal_places=2, color=YELLOW_A)
        eq5_p3 = MathTex(r"\sin x)^2 = ")
        k_num3_3 = DecimalNumber(0, num_decimal_places=2, color=YELLOW_A)
        
        eq5 = VGroup(eq5_p1, k_num3_1, eq5_p2, k_num3_2, eq5_p3, k_num3_3).arrange(RIGHT, buff=0.05).to_edge(UP).set_z_index(2)
        
        eq5.add_updater(lambda m: m.arrange(RIGHT, buff=0.05).to_edge(UP))
        k_num3_1.add_updater(lambda m: m.set_value(k_tracker3.get_value()))
        k_num3_2.add_updater(lambda m: m.set_value(k_tracker3.get_value()))
        k_num3_3.add_updater(lambda m: m.set_value(k_tracker3.get_value()))

        color5 = random.choice(colors)
        curve5 = always_redraw(lambda: axes4.plot_implicit_curve(
            lambda x, y: (x - k_tracker3.get_value()*np.cos(y))**2 + (y - k_tracker3.get_value()*np.sin(x))**2 - k_tracker3.get_value(), color=color5
        ))

        self.play(Write(eq5), Create(curve5))
        self.play(k_tracker3.animate.set_value(16.79), run_time=10, rate_func=linear)
        self.play(FadeOut(eq5), FadeOut(curve5), FadeOut(axes4))