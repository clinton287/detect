import base64
import smtplib
from io import BytesIO
import cv2
import keras
from keras.preprocessing import image
import numpy as np
import secure_smtplib  # Import the secure_smtplib instead of smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import Image
from flask import Flask, request, jsonify
from numpy.random._examples.cython.extending import x

app = Flask(__name__)

@app.route('/Attire_Detection', methods=['POST'])
def Attire_Detection():
    # Step 1: Load the model from the .h5 file
    model = keras.models.load_model('attiredetectionmodel.h5')

    # Captuare video through webcam
    #cap = face_recognition.load_image_file('Anoop1.png')
    image_dat = request.form['image']
    image1 = base64.b64decode(image_dat)
    image = np.array(Image.open(BytesIO(image1)))
    # converttoRGB
    imgS = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 3: Make predictions
    predictions = model.predict(x)

    # Step 4: Interpret the predictions (specific to your model and task)
    predicted_class = np.argmax(predictions)
    print("Predicted class:", predicted_class)

    # Check if the predicted class is 0 (assuming class 0 represents informal attire)
    if predicted_class == 0:
        # Send an email alert
        sender_email = 'davidpaulsalt@gmail.com'
        sender_password = 'rdixapdebzdngrtj'
        receiver_email = 'Clinton.Paul@Vismayacorp.com'

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = 'Attire Detection'

        # Attach the image to the email
        with open(image_dat, 'rb') as img_file:
            image_data = img_file.read()

        image_attachment = MIMEImage(image_data, name='informal_attire.jpg')
        msg.attach(image_attachment)

        # Add text to the email body
        body = "Informal attire detected!"
        msg.attach(MIMEText(body, 'plain'))

        # Send the email using SMTP
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print("Email alert sent successfully.")
        except Exception as e:
            print("Error while sending the email:", e)
    else:
        print("No alert sent.")



        # Showing the webcam output
    #cv2.imshow('result', imgS)
    #key = cv2.waitKey(0)
    # Return the result as JSON response
    return jsonify(msg['Subject']), 200


if __name__ == '__main__':
    app.run()


