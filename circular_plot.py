
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.lines as lines
from flask import Flask, render_template, request, session
import os
from werkzeug.utils import secure_filename
from adjustText import adjust_text
import collections 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=("POST", "GET"))
def get_data():
    if request.method == 'POST':
        file = request.files['upload-file']
        data = pd.read_excel(file, sheet_name=0)
        data.dropna()
        #sheet numarasını ayarla
        plt.style.use('_mpl-gallery')
        x = list((data['Toplam_x']))
        y = list((data['Toplam_y']))
        size = list((data['Toplam_s']))
        values= list(data['Patent'])
        K1 = list(data['K1'])
        K2 = list(data['K2'])
        K3 = list(data['K3'])
        K4 = list(data['K4'])
        K5 = list(data['K5'])
        K6 = list(data['K6'])
        K7 = list(data['K7'])
        K8 = list(data['K8'])
        K9 = list(data['K9'])
        K10 = list(data['K10'])
        x_list = []
        y_list = []
        for x_near in x:
            if pd.isna(x_near):
                pass
            else:                
                x_list.append("%.2f" % x_near)

        for y_near in y:
            if pd.isna(y_near):
                pass
            else:                
                y_list.append("%.2f" % y_near)
         
         
        x_ort = np.nanmean(x)
        x_min = np.nanmin(x)
        x_max = np.nanmax(x)
        
        y_ort = np.nanmean(y)
        y_min = np.nanmin(y)
        y_max = np.nanmax(y)
        
        bolge_1 = []
        bolge_2 = []
        bolge_3 = []
        bolge_4 = []
        bolge_yok = []
        
        new_x_list = [item for item, count in collections.Counter(x_list).items() if count > 1] 
        new_y_list = [item for item, count in collections.Counter(y_list).items() if count > 1] 
        list_control = []
        repeat_val = []
        for label, x_val, y_val in zip(values, x, y):
            if pd.isna(label):
                pass
            else:
                if (x_min<=x_val and x_ort >= x_val) and (y_val <= y_max and  y_val >= y_ort):
                    bolge_1.append(label)
                elif(x_min<=x_val and x_ort >= x_val) and (y_val <= y_ort and  y_val >= y_min):
                    bolge_2.append(label)
                elif(x_ort<=x_val and x_max >= x_val) and (y_val <= y_max and  y_val >= y_ort):
                    bolge_3.append(label)
                elif(x_ort<=x_val and x_max >= x_val) and (y_val <= y_ort and  y_val >= y_min):
                    bolge_4.append(label)
                else:
                    bolge_yok.append(label)
                

        arr = np.array(list_control)
        vals, inverse, count = np.unique(arr,
                                 return_inverse=True,
                                 return_counts=True,
                                 axis=0)
        out = np.where(count[inverse] > 1)[0]
        outx = np.where(count[inverse] <= 1)[0]
        deneme = 0
    class List(list):
        def __setitem__(self, index, value):
            self.extend([None] * ((max(index.start, index.stop - 1) if isinstance(index, slice) else index) - len(self) + 1))
            super().__setitem__(index, value)
    groups_col = List()
    for bolge1_control in bolge_1:
        if bolge1_control in values:
            groups_col[values.index(bolge1_control)] = 1
            
    for bolge2_control in bolge_2:
        if bolge2_control in values:
            groups_col[values.index(bolge2_control)] = 2
    
    for bolge3_control in bolge_3:
        if bolge3_control in values:
            groups_col[values.index(bolge3_control)] = 3
    
    for bolge4_control in bolge_4:
        if bolge4_control in values:
            groups_col[values.index(bolge4_control)] = 4
    
    data['Groups'] = pd.Series(groups_col)
    groups = list(data['Groups'])
    
    def get_label_rotation(angle, offset):
    # Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle + offset)
        if angle <= np.pi:
            alignment = "right"
            rotation = rotation + 180
        else: 
            alignment = "left"
        return rotation, alignment

    def add_labels(angles, valuess, labels, offset, ax):
        padding = 4
    
        for angle, value, label, in zip(angles, valuess, labels):
            angle = angle
        
        # Obtain text rotation and alignment
            rotation, alignment = get_label_rotation(angle, offset)

        # And finally add the text
            ax.text(
                x=angle, 
                y=value + padding, 
                s=label, 
                ha=alignment, 
                va="center", 
                rotation=rotation, 
                rotation_mode="anchor"
            ) 
       
    OFFSET = np.pi / 2
    PAD = 3
    values = [values for values in values if str(values) != 'nan']
    groups = [groups for groups in groups if str(groups) != 'nan']
    values_g = [values for _,values in sorted(zip(groups,values))]
    new_i = [values for values in values if str(values) != 'nan']
    
    for index,val in enumerate(values):
        if (values.index(val) != values_g.index(val)):
                new_i[(values_g.index(val))] = values.index(val)
        else: 
                new_i[(values_g.index(val))] =  (values.index(val))
                    
    list_K = ['K1','K2','K3','K4', 'K5','K6','K7','K8','K9','K10']
    k_dec = ['Item1','Item2','Item3','Item4', 'Item5','Item6','Item7','Item8','Item9','Item10']
    #her bir kriter için döngü halinde getiriyor.
    
    for k_degree,k_,k_desc in zip([K1,K2,K3,K4, K5,K6,K7,K8,K9,K10],list_K,k_dec):   
        
        k_degree = [k_degree[i] for i in new_i]
            
        k_degree = [k_degree for k_degree in k_degree if str(k_degree) != 'nan']
    
        ANGLES_N = len(k_degree)
        ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)
        WIDTH = (2 * np.pi) / len(ANGLES)

        offset = 0
        IDXS = []
        GROUPS_SIZE = [len(bolge_1), len(bolge_2), len(bolge_3), len(bolge_4)]
        for size in GROUPS_SIZE:
            IDXS += list(range(offset , offset + size ))
            offset += size 
        fig1, ax = plt.subplots(figsize=(20, 10), subplot_kw={"projection": "polar"})
        ax.set_theta_offset(OFFSET)
        ax.set_ylim(-25, 25)
        ax.set_frame_on(False)
        ax.xaxis.grid(False)
        ax.yaxis.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])

        GROUPS_SIZE = [len(bolge_1), len(bolge_2), len(bolge_3), len(bolge_4)]
        COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]
        ax.bar(
            ANGLES[IDXS], k_degree, width=WIDTH, color=COLORS, 
            edgecolor="white", linewidth=2
        )     
        add_labels(ANGLES[IDXS], k_degree, values_g,  OFFSET, ax)
      
        offset = 0 
        #kriter no yaz plt üstüne
        k_ = str(k_ + '\n' + k_desc)
        ax.text(
                0, -25, k_, color="#2451B3", fontsize=20, 
                fontweight="bold", ha="center", va="center"
        )
        #bölge adlarını plt üstüne ekliyoruz
        
        for group, size in zip(["BÖLGE 1", "BÖLGE 2", "BÖLGE 3", "BÖLGE 4"], GROUPS_SIZE):
            x1 = np.linspace(ANGLES[offset], ANGLES[offset + size - 1], num=len(values))
            ax.plot(x1, [-5] * len(values), color="#333333")
            
            ax.text(
                np.mean(x1), -10, group, color="#333333", fontsize=14, 
                fontweight="bold", ha="center", va="center"
            )

            x2 = np.linspace(ANGLES[offset], ANGLES[offset - 1], num=50)
            ax.plot(x2, [20] * 50, color="#bebebe", lw=0.8)
            ax.plot(x2, [40] * 50, color="#bebebe", lw=0.8)
            ax.plot(x2, [60] * 50, color="#bebebe", lw=0.8)
            ax.plot(x2, [80] * 50, color="#bebebe", lw=0.8)
    
            offset += size
              
        plt.show()
    return None

if __name__ == '__main__':
    app.run(debug=True)
    

