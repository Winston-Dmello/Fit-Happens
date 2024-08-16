import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_pie_chart(data, labels):
    # Create a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    
    # Save it to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode to base64 to embed in HTML
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    # Close the plot
    plt.close()
    
    return img_base64
