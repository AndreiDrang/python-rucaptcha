from python_rucaptcha import MediaCaptcha

"""
!!!ВАЖНО!!!
Обязательно, перед работой с данным модулем, - создайте папку "mediacaptcha_audio"
!!!ВАЖНО!!!
"""

"""
Этот пример показывает то как нужно работать с модулем для распознования аудио капчи,
на примере нашего сайта и скачаных зарание аудиофайлов.
В общем случае вам потребуется получение:
1. Скачать аудиофайл в зарание созданную папку "mediacaptcha_audio", либо же передать ссылку для скачивания на файл
2. Передать этот параметр в метод MediaCaptcha и так же указать тип капчи из которой получен аудиофайл recaptchavoice, solveaudio.
"""
# Введите ключ от рукапчи из своего аккаунта
RUCAPTCHA_KEY = ''
# Примеры ссылок для различных типов капчи
solve_media_link = "http://85.255.8.26/static/media/solvemedia_audio/solvemedia_runphrough.mp3"
recaptcha_media_link = "http://85.255.8.26/static/media/solvemedia_audio/recaptcha_55914.mp3"
# Примеры файлов для различных типов капчи
solve_media_file = "solvemedia_pzalcbniuf.mp3"
recaptcha_media_file = "recaptcha_55914.mp3"

"""
Тут нужно воспользоваться бибилотекой.
Данный пример показывает работу библиотеки с ссылками, для двух разных выдов капчи
"""
solve_audio_link_answer = MediaCaptcha.MediaCaptcha(RUCAPTCHA_KEY, solveaudio=True).captcha_handler(audio_download_link=solve_media_link)
recaptcha_audio_link_answer = MediaCaptcha.MediaCaptcha(RUCAPTCHA_KEY, recaptchavoice=True).captcha_handler(audio_download_link=recaptcha_media_link)
print("SolveMedia link answer is: "+solve_audio_link_answer)
print("ReCaptcha link answer is: "+recaptcha_audio_link_answer)


"""
Тут нужно воспользоваться бибилотекой.
Данный пример показывает работу библиотеки с файлами, для двух разных выдов капчи
"""
solve_audio_file_answer = MediaCaptcha.MediaCaptcha(RUCAPTCHA_KEY, solveaudio=True).captcha_handler(audio_name=solve_media_file)
recaptcha_audio_file_answer = MediaCaptcha.MediaCaptcha(RUCAPTCHA_KEY, recaptchavoice=True).captcha_handler(audio_name=recaptcha_media_file)
print("SolveMedia file answer is: "+solve_audio_file_answer)
print("ReCaptcha file answer is: "+recaptcha_audio_file_answer)
