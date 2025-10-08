import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import Image
import os

class ImageToPDFConverter:
  def __init__(self, root):
    self.root = root
    self.image_path = []
    self.output_pdf_name = tk.StringVar()
    self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    
    self.initialize_ui()
    
  def initialize_ui(self):
    
    #creating 'Image2Pdf Coverter' label
    title_label = tk.Label(self.root, text="Image2Pdf Converter", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)
    
    #creating 'Select images' button
    select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
    select_images_button.pack(pady=(0,10))
    
    #creating a listbox for displaying the selected images
    self.selected_images_listbox.pack(pady=(0,10), fill=tk.BOTH, expand=True)
    
    #creating label for entering the PDF name
    label = tk.Label(self.root, text="Enter output PDF name:")
    label.pack()
    
    #creating a Entry for the PDF name
    pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
    pdf_name_entry.pack()
    
    #creating 'Convert to PDF' button
    convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
    convert_button.pack(pady=(20,40))
    
  def select_images(self):
    
    #display file explorer to select the images with the accepted file formats
    self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    
    #updating the file in the listbox
    self.update_selected_images_listbox()
    
  def update_selected_images_listbox(self):
    
    #deleting the prev files from the listbox display
    self.selected_images_listbox.delete(0, tk.END)
    
    for image_path in self.image_paths:
      #splitting the whole path name and giving out just the file name
      _, image_path = os.path.split(image_path)
      
      #inserting the file name alone to the listbox
      self.selected_images_listbox.insert(tk.END, image_path)
      
  def convert_images_to_pdf(self):
    
    #checking if the user have added the pdf name
    if not self.image_paths:
      return
    
    #if the user had not entered the pdf name, name it "output.pdf"
    output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
    
    #creating the pdf with the pdf name and giving the page size
    pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))
    
    #to insert the slected images to pdf
    for image_path in self.image_paths:
      #opening the images with the help of Pillow library
      img = Image.open(image_path)
      
      #defining the default width and height of the image
      available_width = 540
      available_height = 720
      
      #to insert the images in each one single page in center of the page 
      scale_factor = min(available_width / img.width, available_height / img.height)
      
      #to place the image in the centre of the page
      new_width = img.width * scale_factor
      new_height = img.height * scale_factor
      x_centered = (612 - new_width) / 2
      y_centered = (792 - new_height) / 2
      
      #initializing the margin and giving it white color
      pdf.setFillColorRGB(255, 255, 255)
      pdf.rect(0,0,612,792,fill=True)
      
      #adding the image on the white page
      pdf.drawInlineImage(img, x_centered, y_centered, width= new_width, height=new_height)
      pdf.showPage()
      
    #saving the pdf
    pdf.save()
      
    
    
def main():
  root=tk.Tk()
  root.title("Image2Pdf") #adding titlename
  converter = ImageToPDFConverter(root)
  root.geometry("400x650") #size of the app
  root.mainloop()
  
if __name__ == "__main__":
  main()
  
  
  