import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import os
import threading
import webbrowser

root = tk.Tk()
root.title("Meal search")

meals = []
meal_images = {}

def api(event):
    
    global link1
    curItem = tree.focus()
    
    current_id = tree.item(curItem)["values"][0]

    response = requests.get("https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + str(current_id))
    json_data = response.json()
    Mealinfostr = f"""
Name: {json_data.get("meals")[0].get("strMeal")}
Category: {json_data.get("meals")[0].get("strCategory")}
Region: {json_data.get("meals")[0].get("strArea")}
"""
    Mealinfo.configure(text=Mealinfostr)
    instructionbox.delete(1.0, tk.END)
    instructionbox.insert(tk.INSERT, json_data.get("meals")[0].get("strInstructions"))
    

    thumbnail_image = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\\thumbnails\\" + str(current_id) + ".jpg").resize((200, 200)))
    
    thumbnail.configure(image=thumbnail_image)
    thumbnail.image = thumbnail_image
    
    ingredientbox.delete(1.0, tk.END)
    if json_data.get("meals")[0].get("strYoutube") != None:
        
        link1.pack()
        link1.bind("<Button-1>", lambda e: callback(json_data.get("meals")[0].get("strYoutube")))
    else:
        link1 = tk.Label(root, text="No YouTube video available", fg="gray")
    for i in range(20):
        try:
            if json_data.get("meals")[0].get(f"strIngredient{i+1}") != "":
                ingredientbox.insert(tk.INSERT, json_data.get("meals")[0].get(f"strIngredient{i+1}") +" : "+ json_data.get("meals")[0].get(f"strMeasure{i+1}") + "\n")
        except TypeError:
            pass

def download_image(meal):
    thumbnail_path = os.path.dirname(os.path.realpath(__file__)) + "/thumbnails/" + meal.get("idMeal", "") + ".jpg"
    if not os.path.exists(thumbnail_path):
        with open(thumbnail_path, "wb") as f:
            response = requests.get(meal.get("strMealThumb", ""))
            f.write(response.content)
            print("Downloaded " + meal.get("strMeal", ""))
    # Now that the image is downloaded, trigger the update in the main thread
    root.after(0, update_tree_with_image, meal, thumbnail_path)

def update_tree_with_image(meal, image_path):
    img = Image.open(image_path).resize((50, 50))
    image_tk = ImageTk.PhotoImage(img)
    meal_images[meal["idMeal"]] = image_tk
    tree.insert(parent='', index="end", values=(meal.get("idMeal", ""), meal.get("strMeal", ""), meal.get("strCategory", ""), meal.get("strArea", "")), image=image_tk, open=True)

def delete_all_items():
    tree.delete(*tree.get_children())

def on_entry_key_release(event):
    delete_all_items()
    meals.clear()
    if search_type.get() == 1:
        url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + entry.get()
    elif search_type.get() == 2:
        url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=" + entry.get()
    elif search_type.get() == 3:
        url = "https://www.themealdb.com/api/json/v1/1/filter.php?a=" + entry.get()
    elif search_type.get() == 4:
        url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + entry.get()
    elif search_type.get() == 5:
        url = "https://www.themealdb.com/api/json/v1/1/filter.php?i=" + entry.get()
    response = requests.get(url)
    if response.status_code != 200:
        print("Something went wrong! Status code: " + str(response.status_code))
        return 
    json_data_search = response.json()
    try:
        for meal in json_data_search.get("meals", []):
            meals.append((meal.get("idMeal", ""), meal.get("strMeal", ""), meal.get("strCategory", ""), meal.get("strArea", "")))
            dl_thread = threading.Thread(target=download_image, args=(meal,))
            dl_thread.start()
    except TypeError:
        pass

def callback(url):
    webbrowser.open_new(url)

style = ttk.Style()
style.configure('Treeview', rowheight=50)  # increase height 

tk.Label(root, text="Meal finder").pack()

tk.Label(root, text="Search for a meal").pack()
entry = tk.Entry(root)
entry.pack()
entry.bind("<KeyRelease>", on_entry_key_release)
search_type = tk.IntVar()
search_type.set(1)
search_frame = tk.Frame(root)
tk.Radiobutton(search_frame, text="Name", variable=search_type, value=1).pack(side=tk.LEFT)
tk.Radiobutton(search_frame, text="Category", variable=search_type, value=2).pack(side=tk.LEFT)
tk.Radiobutton(search_frame, text="Region", variable=search_type, value=3).pack(side=tk.LEFT)
tk.Radiobutton(search_frame, text="ID", variable=search_type, value=4).pack(side=tk.LEFT)
tk.Radiobutton(search_frame, text="Ingredient", variable=search_type, value=5).pack(side=tk.LEFT)
search_frame.pack()


columns = ('id', 'name', 'category', "region")
tree = ttk.Treeview(root, columns=columns)
tree.heading('id', text='ID')
tree.heading('name', text='Name')
tree.heading('category', text='Category')
tree.heading('region', text='Region')

tree.column("id", width=50)
tree.column("name", width=150)
tree.column("category", width=100)
tree.column("region", width=100)

tree.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)

tree.bind('<<TreeviewSelect>>', api)

Mealinfostr = """
Name: 
Category:
Region:
"""

thumbnail = tk.Label(root)
thumbnail.pack()
Mealinfo = tk.Label(root, text=Mealinfostr)
Mealinfo.pack()
link1 = tk.Label(root, text="YouTube Video", fg="blue", cursor="hand2")
link1.pack()

instructionbox = tk.Text(root, width=50, height=10)
instructionbox.pack(side=tk.LEFT)
scrollbar_instructions = ttk.Scrollbar(root, orient=tk.VERTICAL, command=instructionbox.yview)
instructionbox.configure(yscrollcommand=scrollbar_instructions.set)
scrollbar_instructions.pack(side=tk.LEFT,fill=tk.Y)

ingredientbox = tk.Text(root, width=50, height=10)
ingredientbox.pack(side=tk.LEFT)
scrollbar_ingredient = ttk.Scrollbar(root, orient=tk.VERTICAL, command=ingredientbox.yview)
ingredientbox.configure(yscrollcommand=scrollbar_ingredient.set)
scrollbar_ingredient.pack(side=tk.LEFT,fill=tk.Y)

root.mainloop()