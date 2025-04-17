import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

con = sqlite3.connect("project.db")
df = pd.read_sql_query("""
    Select id, name, sum(capacity) as total
    from plants
    group by id, name

""", con)

df.plot(x="id", y="total", kind="bar", title="Total Capacity by Plant ID")
plt.xlabel("Plant ID")
plt.ylabel("Total Capacity")
plt.tight_layout()
plt.show()



product_id = 2
df = pd.read_sql_query(f"""
    SELECT m.name, pm.quantity
    FROM product_materials pm
    JOIN materials m ON pm.material_id = m.id
    WHERE pm.product_id = {product_id}
""", con)


df.set_index('name').plot.pie(y='quantity', autopct='%1.1f%%', legend=False)
plt.title(f"Distribuție materiale pentru produs {product_id}")
plt.ylabel("")
plt.tight_layout()
plt.show()

con.close()