set -o errexit  #Para que el script se detenga en caso de que algun comando falle

pip install -r requirements.txt

python manage.py collectstatic --no-input #recopilar todos los archivos estáticos de una aplicación Django (como CSS, JavaScript e imágenes) y copiarlos en un único directorio centralizado definido en la variable STATIC_ROOT

python manage.py migrate