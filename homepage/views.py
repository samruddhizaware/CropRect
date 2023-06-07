# from django.http import request
from django.shortcuts import render
from django.forms import forms
from .forms import TestClassForm
import os
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, plot_confusion_matrix, confusion_matrix
import pickle
import io

import warnings
warnings.filterwarnings("ignore")






def index(request):
    
    form = TestClassForm()
    final_predict=''
    if request.method=="POST":
        form = TestClassForm(request.POST)
        if form.is_valid():
            form.save()

        data = pd.read_csv(('./Data/Crop_recommendation.csv'))
        all_columns = data.columns[:-1]
        label_encoder = LabelEncoder()
        X = data[all_columns]
        y = label_encoder.fit_transform(data["label"])
        
        label_dict = {}
        for i in range(22):
            label_dict[i] = label_encoder.inverse_transform([i])[0]
        # print(label_dict)

        X_train, X_test, y_train, y_test = train_test_split(X.values, y, test_size = 0.2, random_state = 0)
        # print(f"Train Data: {X_train.shape}, {y_train.shape}")
        # print(f"Train Data: {X_test.shape}, {y_test.shape}")

        
        error_rate = []
        for i in range(1, 50):
            pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors = i))
            pipeline.fit(X_train, y_train)
            predictions = pipeline.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            # print(f"Accuracy at k = {i} is {accuracy}")
            error_rate.append(np.mean(predictions != y_test))
        
        
        knn_pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors = 4))
        knn_pipeline.fit(X_train, y_train)

        d = request.POST
        list_input= []
        for key,values in d.items():
            list_input.append(values)
        # print(list_input[1:])
        list_input = list_input[1:]
        model_input = [[float(i) for i in list_input]]
        pred = knn_pipeline.predict(model_input)
        final_predict = label_dict[pred[0]]

        # print(model_input)
    
    context= {'form':form, 'final_predict': final_predict}
    return render(request, "index.html",context)
