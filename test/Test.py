import subprocess
import os
def render_latex_to_png(latex_equation, output_file):
    katex_command = ['katex', '-o', output_file, '--format', 'png', latex_equation]
    
    try:
        # subprocess.run(katex_command, check=True)
        # print(f"Equation rendered and saved as {output_file}")
        os.system(" ".join(katex_command))
    except subprocess.CalledProcessError:
        print("Error rendering equation")

# Usage
latex_equation = r"\frac{1}{2} \cdot \sqrt{x^2 + y^2}"
output_file = "equation.png"
render_latex_to_png(latex_equation, output_file)
