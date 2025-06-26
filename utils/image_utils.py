import os
from kivy.app import App
from datetime import datetime
from functools import partial

def file_picker_android(myapp):
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    from android import activity, mActivity

    request_permissions([Permission.READ_EXTERNAL_STORAGE])
    Intent = autoclass('android.content.Intent')
    intent = Intent(Intent.ACTION_GET_CONTENT)
    intent.setType("image/*")
    intent.addCategory(Intent.CATEGORY_OPENABLE)

    mActivity.startActivityForResult(intent, 1001)
    activity.bind(on_activity_result=partial(on_activity_result, myapp))

def on_activity_result(myapp, request_code, result_code, intent):
    if request_code != 1001 or result_code != -1:
        return

    from android import activity
    from jnius import cast

    uri = intent.getData()
    if uri is None:
        print("No URI returned.")
        return

    try:
        # Read the input stream and save it to private storage
        copy_image_from_uri(myapp, uri)
    except Exception as e:
        print(f"Error handling selected file: {e}")

    activity.unbind(on_activity_result=on_activity_result)

def copy_image_from_uri(myapp, uri):
    from android import mActivity
    from jnius import autoclass, cast

    ContentResolver = autoclass("android.content.ContentResolver")
    InputStreamReader = autoclass("java.io.InputStreamReader")
    BufferedInputStream = autoclass("java.io.BufferedInputStream")

    resolver = mActivity.getContentResolver()
    input_stream = resolver.openInputStream(uri)

    # Create a filename and path
    filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    app_dir = os.path.join(App.get_running_app().user_data_dir, "photos")
    os.makedirs(app_dir, exist_ok=True)
    file_path = os.path.join(app_dir, filename)

    # Copy the file
    with open(file_path, "wb") as out_file:
        buf = bytearray(1024)
        while True:
            read_bytes = input_stream.read(buf)
            if read_bytes == -1:
                break
            out_file.write(buf[:read_bytes])

    input_stream.close()

    print(f"Saved file to: {file_path}")
    myapp.fourth_screen.img.source = file_path
    myapp.fourth_screen.img.reload()        