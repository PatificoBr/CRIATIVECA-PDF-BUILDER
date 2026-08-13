import os
from natsort import natsorted
from app.pdf import PDFBuilder
from app.utils import get_file_size

input_folder = 'input'
images = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
images = natsorted(images)

builder = PDFBuilder()
output = 'output/test_builder.pdf'
if not os.path.exists('output'):
    os.makedirs('output')

success, msg = builder.build(
    images,
    output,
    'Teste',
    'Sub',
    logo_path=None,
    optimize_images=True,
    dpi=150,
    jpeg_quality=50,
    conversion_mode='auto',
)
print('Success:', success, 'Message:', msg)
if success:
    print('Final size:', get_file_size(output))
