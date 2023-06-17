from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.conf import settings
from django.http import JsonResponse

import os
import re
import pickle
import warnings
warnings.filterwarnings(action='ignore')


import nltk
nltk.data.path.append(settings.NLTK_DATA)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

from api.api.serializers import CategoriesSerializer, ModelPredictionSerializer


def preprocess_text(text, use_stemming=False, use_lemmatization=True):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and digits
    text = re.sub('[^a-zA-Z\s]', '', text)
    text = re.sub('\d+', '', text)

    # Tokenize text
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Apply stemming and/or lemmatization
    if use_stemming:
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]

    if use_lemmatization:
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]

    # Join words back into a string
    text = ' '.join(words)

    return text


class CategoriesView(GenericAPIView):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return []

    def get(self, request):
        categories = [
            "other",
            "needs_troubleshooting",
            "card_queries_or_issues",
            "top_up_queries_or_issues"
        ]
        return Response(categories, status=status.HTTP_200_OK)
    

class ModelPredictionView(GenericAPIView):
    serializer_class = ModelPredictionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        model_name = serializer.validated_data.get('model_name')
        user_query = serializer.validated_data.get('text')
        print(model_name)
        # Preprocess the user query
        preprocessed_query = preprocess_text(user_query)

        # Choose the appropriate model based on the model_name parameter
        model_file = settings.MODELS.get(model_name)

        if model_file is not None:
            # Construct the absolute file path
            model_file_path = os.path.join(settings.BASE_DIR, model_file)

            # Load the selected model
            with open(model_file_path, 'rb') as file:
                model = pickle.load(file)

            # Make predictions using the loaded model
            predicted_category = model.predict([preprocessed_query])

            # Return the predicted category as JSON response
            return JsonResponse({'message': predicted_category[0]})
        else:
            return JsonResponse({'error': 'Invalid model_name. Please choose from the available models.'})