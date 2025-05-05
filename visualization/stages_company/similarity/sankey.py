import plotly.graph_objects as go
import matplotlib.colors as mcolors

# Labels for nodes across all three layers
labels = [
    # Science Layer
    "Monitoring systems", "Rehabilitation", "Dementia", "Surgery and Cancer", "Infectious diseases",
    "AI", "Chronic diseases",
    # Technology Layer
    "Sensor systems", "IoT", "Hearing aid", "Medical", "Telemedicine", "AI and Robots",
    # Business Layer
    "AI and Robots", "Telemedicine", "Medical", "Digital wellness", "Healthcare"
]


colors = [
    # Science colors
    '#069AF3', 'green', '#0000FF', 'red', 'orange', 'purple', "#6C733D",
    # Technology colors
    'orange', '#0000FF', 'green', 'red', '#069AF3', 'purple',
    # Business colors
    'purple', '#069AF3', 'red', 'green', 'orange'
]


def adjust_transparency(hex_color, alpha=0.5):
    # Convert hex to RGB, which is in [0,1] range
    rgb = mcolors.hex2color(hex_color)
    # Add the alpha channel
    return f"rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, {alpha})"

# Your original colors array
original_colors = [
    '#069AF3', 'green', '#0000FF', 'red', 'orange', 'purple', "#6C733D",
    'orange', '#0000FF', 'green', 'red', '#069AF3', 'purple',
    'purple', '#069AF3', 'red', 'green', 'orange'
]

# Adjusting the transparency of each color
transparent_colors = [adjust_transparency(color, 0.3) for color in original_colors]

# Now use 'transparent_colors' in your Sankey diagram setup

# Matrix from Science to Technology
matrix_sci_to_tech = [
    [0.652393681, 0.06302722, 0.618286971, 0.894029147, 0.439260324, 0.235462843],
    [0.715733732, 0.453300494, 0.112104165, 0.678848212, 0.834593424, 0.397034037],
    [0.663452111, 0.866009397, 0.142537355, 0.548772431, 0.368472302, 0.464381375],
    [0.076982402, 0.572952859, 0.520192554, 0.212790606, 0.707988044, 0.947170779],
    [0.555964075, 0.654475647, 0.841667986, 0.077263535, 0.488636652, 0.411463586],
    [0.461844242, 0.214601432, 0.605440644, 0.902785385, 0.176652183, 0.418872028],
    [0.441899381, 0.974514838, 0.325340295, 0.276186599, 0.34009471, 0.662861854]
]

# Matrix from Technology to Business
matrix_tech_to_biz = [
    [0.702698672, 0.285466677, 0.170785931, 0.759762559, 0.580268927],
    [0.083917745, 0.579316322, 0.428989922, 0.828196851, 0.736568185],
    [0.62118375, 0.905108761, 0.194224787, 0.235434594, 0.423630384],
    [0.87816744, 0.171186625, 0.678319649, 0.581648181, 0.112401274],
    [0.439231662, 0.321196649, 0.651627868, 0.278772067, 0.845358396],
    [0.190365718, 0.625111629, 0.881134149, 0.334736651, 0.528019908]
]


source = []
target = []
value = []

threshold = 0.3  # Threshold to control flow visibility

# Process first matrix (Science to Technology)
for i in range(len(matrix_sci_to_tech)):
    for j in range(len(matrix_sci_to_tech[i])):
        if matrix_sci_to_tech[i][j] > threshold:
            source.append(i)  # Science layer index
            target.append(7 + j)  # Offset by 7 to start at the technology layer
            value.append(matrix_sci_to_tech[i][j])

# Process second matrix (Technology to Business)
for i in range(len(matrix_tech_to_biz)):
    for j in range(len(matrix_tech_to_biz[i])):
        if matrix_tech_to_biz[i][j] > threshold:
            source.append(7 + i)  # Technology layer index
            target.append(13 + j)  # Offset by 13 to start at the business layer
            value.append(matrix_tech_to_biz[i][j])


fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=10,
        thickness=15,
        line=dict(color="black", width=0.1),
        label=labels,
        color=transparent_colors,  # Use transparent colors here
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=[transparent_colors[s] for s in source],  # Apply transparent colors to links based on source
        line=dict(
            color=['rgba(0,0,0,0.1)' if v <= 0.8 else 'rgba(255,0,0,1)' for v in value]  # Highlight values over 0.8
        )
    )
)])


fig.update_layout(title_text="Sankey Diagram: Science -> Technology -> Business", font_size=12)
fig.show()


