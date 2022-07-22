import cv2
import numpy as np
from flask import Flask, jsonify, request
import urllib.request
from werkzeug.utils import secure_filename
app = Flask(__name__)
import easyocr

@app.route('/api/cart/detection', methods = ['POST'])
def name_detec():
   cart = "No"
   name1 = " "
   name2 = " "
   dateNaiss = " "
   dateExp = " "
   idCard = " "
   adresse = " "
   royaume = ["ROYAUME", "MAROC", "ROYAUME DU MAROC", "DU MAROC"]
   fullName = ["CARTE", "NATIONALE", "DIDENTITE", "D'IDENTITE","CARTE NATIONALE DIDENTITE"]
   dateNaissance = ["Ne le", "Né", "Né le"]
   dateExpiration = ["Valable jusqu'au", "Valable jusqu au", "Valable"]
   image = request.files['image']
   filename = secure_filename(image.filename)
   image.save('a33.jpg')

   reader = easyocr.Reader(['en'], gpu=False)
   result = reader.readtext('a33.jpg')
   index = 0
   outresult = []
   textDtect = " "
   print(result)
   index1 = 0
   for word1 in result:
      if (word1[2] > 0.50 or any(x in word1[1] for x in dateNaissance) or any(x in word1[1] for x in dateExpiration)) and len(word1[1]) > 2:
         if any(x in word1[1] for x in dateNaissance) and outresult[index1-1][1].isalpha() == False:
            k = outresult[index1-1]
            outresult[index1-1] = word1
            outresult.append(k)
         else:
            outresult.append(word1)

         textDtect = textDtect + " " + word1[1]
         index1 = index1 + 1
   print(outresult)
   if any(x in textDtect for x in royaume):
      cart = "Yes"
      for word in outresult:
         if any(x in word[1] for x in fullName):
            name1 = outresult[index + 1][1]
            name2 = outresult[index + 2][1]

         if any(x in word[1] for x in dateNaissance):
            name1 = outresult[index - 2][1]
            name2 = outresult[index - 1][1]
            dateNaiss = outresult[index + 1][1]
            for t in dateNaiss:
               if t.isnumeric() == False:
                  dateNaiss = dateNaiss.replace(t, ".", 1)


         if any(x in word[1] for x in dateExpiration):
            if outresult[index + 1][1][0:2].isnumeric():
               dateExp = outresult[index + 1][1]
               for t in dateExp:
                  if t.isnumeric() == False:
                     dateExp = dateExp.replace(t, ".", 1)
               if outresult[index - 1][1][0] == 'a':
                  adresse = outresult[index - 1][1]

         if word[1].isalnum() and word[1].isalpha() == False and len(word[1]) > 4 :
            idCard = outresult[index][1]
            if idCard.isnumeric() and idCard[0] == "1":
               idCard = idCard.replace(idCard[0],"I",1)
            if dateExp == " ":
               if outresult[index -1][1][0:2].isnumeric() :
                  dateExp = outresult[index -1][1]
               elif outresult[index -2][1][0:2].isnumeric() and outresult[index -2][1] != dateNaiss:
                  dateExp = outresult[index -2][1]

               print(outresult[index][1][0:2])


         index += 1
      return jsonify(
         {'carteDetecion': cart, 'firtName': name1, 'lastName': name2, 'dateNaissance': dateNaiss, 'idCard': idCard,
          'dateExp': dateExp, 'adresseNaissance': adresse})
   else:
      return jsonify({'carteDetecion': cart})

if __name__ == '__main__':
    app.run()