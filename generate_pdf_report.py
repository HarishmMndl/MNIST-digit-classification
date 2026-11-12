import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page count
    along with running header and footer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Top Running Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 756, "MNIST Handwritten Digit Classification | Project Documentation & Function Reference")
            self.drawRightString(576, 756, "project.ipynb")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(36, 750, 576, 750)

        # Bottom Running Footer (All Pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(36, 38, 576, 38)
        self.drawString(36, 26, "CNN_Projects | Deep Learning & Computer Vision Analysis")
        self.drawRightString(576, 26, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()


def build_pdf(filename="MNIST_Digit_Classification_Project_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1E3A8A")   # Deep Navy
    secondary_color = colors.HexColor("#0284C7") # Ocean Blue
    text_dark = colors.HexColor("#1E293B")       # Slate 800
    bg_light = colors.HexColor("#F8FAFC")        # Slate 50
    border_color = colors.HexColor("#E2E8F0")

    doc_title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )

    doc_subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E3A8A")
    )

    tbl_header_style = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=text_dark
    )

    tbl_cell_code = ParagraphStyle(
        'TblCellCode',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=text_dark
    )

    story = []

    # Title Banner Block
    banner_data = [
        [
            Paragraph("MNIST Handwritten Digit Classification", doc_title_style),
            Paragraph("<b>Target Notebook:</b> project.ipynb<br/><b>Frameworks:</b> TensorFlow 2.x, OpenCV, NumPy, Seaborn<br/><b>Generated:</b> October 2026", ParagraphStyle('MetaRight', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor("#475569"), alignment=2))
        ],
        [
            Paragraph("<b>Complete Architecture Walkthrough & Function-by-Function Reference Guide</b>", doc_subtitle_style),
            ""
        ]
    ]
    banner_table = Table(banner_data, colWidths=[350, 190])
    banner_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('SPAN', (0, 1), (1, 1)),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(banner_table)
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=8))

    # Executive Summary Box
    summary_html = (
        "<b>Executive Summary:</b> This project explores the end-to-end development, training, evaluation, and practical deployment "
        "of deep learning models for classifying handwritten digits (0–9) using the benchmark <b>MNIST</b> dataset (70,000 images). "
        "The notebook implements a dual-architecture comparison: a baseline <b>Dense Artificial Neural Network (ANN)</b> achieving "
        "<b>97.84% test accuracy</b>, and a spatial-aware <b>Convolutional Neural Network (CNN)</b> achieving a superior <b>99.21% test accuracy</b>. "
        "Furthermore, the project creates an end-to-end <b>Computer Vision inference pipeline</b> using OpenCV to preprocess real-world external "
        "test images (such as <code>5.png</code> and <code>4.png</code>) to perform real-time interactive predictions."
    )
    callout_data = [[Paragraph(summary_html, callout_text)]]
    callout_table = Table(callout_data, colWidths=[540])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # SECTION 1: Project Overview & High-Level Architecture
    story.append(Paragraph("1. Project Architecture & Workflow Overview", h1_style))
    story.append(Paragraph(
        "The project follows a standard machine learning lifecycle structured into 6 sequential phases:",
        body_style
    ))

    phases = [
        ("Phase 1: Data Acquisition & Exploratory Analysis", "Loading the 70,000 MNIST digit images, inspecting array shapes, data types, pixel ranges, and visualizing ground-truth digit samples."),
        ("Phase 2: Data Normalization / Scaling", "Applying Min-Max normalization by dividing raw 8-bit pixel values (0–255) by 255.0 to map input features into the float range [0.0, 1.0]."),
        ("Phase 3: Baseline Neural Network (Dense ANN)", "Building a fully-connected feed-forward network with Flatten, two hidden Dense layers (128 & 64 units with ReLU), and a 10-unit Softmax output layer."),
        ("Phase 4: Diagnostics & Error Analysis", "Generating probability distributions via <code>model.predict()</code>, computing argmax predictions, and plotting a 10x10 Confusion Matrix heatmap to detect digit confusion."),
        ("Phase 5: Advanced Spatial Model (Deep CNN)", "Constructing a 2D Convolutional Neural Network with <code>Conv2D</code>, <code>MaxPooling2D</code>, and <code>Dropout(0.25)</code> to retain spatial relationships and curb overfitting."),
        ("Phase 6: Real-World Predictive System", "Developing an image-processing pipeline using OpenCV (<code>cv2</code>) to load external camera/scan images, convert RGB to Grayscale, resize to 28x28, normalize, and predict.")
    ]

    for title, desc in phases:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 8))

    # Architecture Comparison Table
    story.append(Paragraph("High-Level Model Comparison (ANN vs CNN)", h2_style))
    comp_data = [
        [
            Paragraph("Metric / Feature", tbl_header_style),
            Paragraph("Baseline ANN (model)", tbl_header_style),
            Paragraph("Deep CNN (model_cnn)", tbl_header_style),
            Paragraph("Advantage / Impact", tbl_header_style)
        ],
        [
            Paragraph("Input Transformation", tbl_cell_bold),
            Paragraph("<code>Flatten(28, 28)</code> → 784-dim vector", tbl_cell_style),
            Paragraph("<code>Reshape((28,28,1))</code> (Keeps 2D grid)", tbl_cell_style),
            Paragraph("CNN preserves 2D spatial pixel neighborhoods", tbl_cell_style)
        ],
        [
            Paragraph("Feature Extraction", tbl_cell_bold),
            Paragraph("None (learns global weights directly)", tbl_cell_style),
            Paragraph("2x Conv2D (32, 64) + 2x MaxPool (2x2)", tbl_cell_style),
            Paragraph("Extracts translation-invariant edges & loops", tbl_cell_style)
        ],
        [
            Paragraph("Regularization", tbl_cell_bold),
            Paragraph("None (susceptible to overfitting)", tbl_cell_style),
            Paragraph("<code>Dropout(0.25)</code> before Dense layer", tbl_cell_style),
            Paragraph("Prevents co-adaptation of features", tbl_cell_style)
        ],
        [
            Paragraph("Training Accuracy", tbl_cell_bold),
            Paragraph("~99.30% (after 10 epochs)", tbl_cell_style),
            Paragraph("~99.46% (with 10% validation split)", tbl_cell_style),
            Paragraph("Both models train smoothly with Adam", tbl_cell_style)
        ],
        [
            Paragraph("Test Accuracy (10,000)", tbl_cell_bold),
            Paragraph("<b>97.84%</b>", tbl_cell_bold),
            Paragraph("<b>99.21%</b>", tbl_cell_bold),
            Paragraph("<b>+1.37% gain</b> (~63% test error reduction)", tbl_cell_style)
        ],
        [
            Paragraph("External Image Robustness", tbl_cell_bold),
            Paragraph("Lower (failed on <code>5.png</code>)", tbl_cell_style),
            Paragraph("High (predicts correctly via local patterns)", tbl_cell_style),
            Paragraph("Crucial for real-world digit deployment", tbl_cell_style)
        ]
    ]

    comp_table = Table(comp_data, colWidths=[110, 140, 145, 145])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 14))

    # SECTION 2: Comprehensive Function-by-Function Reference
    story.append(Paragraph("2. Comprehensive Function & Method Reference", h1_style))
    story.append(Paragraph(
        "Below is an exhaustive breakdown of every key library function, method, layer, and API utilized in <code>project.ipynb</code>, "
        "detailing exactly what work it performed and why it was required.",
        body_style
    ))

    func_data = [
        [
            Paragraph("Library / Module", tbl_header_style),
            Paragraph("Function / Method", tbl_header_style),
            Paragraph("What Work It Did in This Project", tbl_header_style),
            Paragraph("Technical Purpose & Why Used", tbl_header_style)
        ],
        # TensorFlow / Keras Dataset & Model
        [
            Paragraph("tensorflow.keras.datasets", tbl_cell_bold),
            Paragraph("<code>mnist.load_data()</code>", tbl_cell_code),
            Paragraph("Downloaded and unpacked the 70,000 MNIST images into 60k training samples and 10k test samples.", tbl_cell_style),
            Paragraph("Standard benchmark loader; automatically splits inputs (X) and ground-truth targets (y).", tbl_cell_style)
        ],
        [
            Paragraph("tensorflow.keras", tbl_cell_bold),
            Paragraph("<code>tf.keras.Sequential([...])</code>", tbl_cell_code),
            Paragraph("Instantiated the model containers for both the baseline ANN (<code>model</code>) and the CNN (<code>model_cnn</code>).", tbl_cell_style),
            Paragraph("Defines a linear stack of neural network layers where tensor data flows sequentially from input to output.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.layers", tbl_cell_bold),
            Paragraph("<code>Flatten(input_shape=(28,28))</code>", tbl_cell_code),
            Paragraph("Transformed each 2D 28x28 pixel matrix into a flat 1D vector of 784 elements in the baseline ANN.", tbl_cell_style),
            Paragraph("Dense layers require 1D vector inputs; Flatten reshapes without altering batch dimensions.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.layers", tbl_cell_bold),
            Paragraph("<code>Dense(units, activation)</code>", tbl_cell_code),
            Paragraph("Created fully connected layers: 128 & 64 units (ReLU) for feature representation, and 10 units (Softmax) for output.", tbl_cell_style),
            Paragraph("Performs matrix multiplication (W·X + b). ReLU adds non-linearity; Softmax outputs normalized probabilities.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.layers", tbl_cell_bold),
            Paragraph("<code>Reshape((28, 28, 1))</code>", tbl_cell_code),
            Paragraph("Converted 2D grayscale matrices (28, 28) into explicit 3D image tensors (28, 28, 1) at the entrance of the CNN.", tbl_cell_style),
            Paragraph("Conv2D operations require explicit channel dimensions (Height x Width x Channels).", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.layers", tbl_cell_bold),
            Paragraph("<code>Conv2D(filters, kernel, activation)</code>", tbl_cell_code),
            Paragraph("Block 1 used 32 filters (3x3); Block 2 used 64 filters (3x3) to convolve over image features.", tbl_cell_style),
            Paragraph("Extracts spatial visual features (edges, curves, loops) while maintaining positional relationship of pixels.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.layers", tbl_cell_bold),
            Paragraph("<code>MaxPooling2D(pool_size=(2,2))</code>", tbl_cell_code),
            Paragraph("Downsampled feature map dimensions by half after each Conv2D block (from 28x28 to 13x13 to 5x5).", tbl_cell_style),
            Paragraph("Reduces spatial footprint, cuts computational cost, and grants spatial translation invariance.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.layers", tbl_cell_bold),
            Paragraph("<code>Dropout(0.25)</code>", tbl_cell_code),
            Paragraph("Randomly deactivated 25% of neurons during each CNN training pass.", tbl_cell_style),
            Paragraph("Acts as an effective regularizer, preventing co-adaptation of neurons and reducing overfitting.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.Model", tbl_cell_bold),
            Paragraph("<code>model.compile(optimizer, loss, metrics)</code>", tbl_cell_code),
            Paragraph("Configured both networks with <code>adam</code> optimizer, <code>sparse_categorical_crossentropy</code>, and <code>accuracy</code>.", tbl_cell_style),
            Paragraph("Compiles the computational graph. Sparse cross-entropy handles integer labels without one-hot encoding.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.Model", tbl_cell_bold),
            Paragraph("<code>model.fit(X, y, epochs, ...)</code>", tbl_cell_code),
            Paragraph("Executed iterative training: ANN trained for 10 epochs; CNN trained for 10 epochs with batch size 64 and 10% validation.", tbl_cell_style),
            Paragraph("Performs forward pass, backpropagation, gradient calculation, and weight optimization.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.Model", tbl_cell_bold),
            Paragraph("<code>model.evaluate(X_test, y_test)</code>", tbl_cell_code),
            Paragraph("Evaluated test loss and accuracy across the 10,000 unseen benchmark samples.", tbl_cell_style),
            Paragraph("Measures unbiased generalization performance on out-of-sample data.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.Model", tbl_cell_bold),
            Paragraph("<code>model.predict(X)</code>", tbl_cell_code),
            Paragraph("Generated raw 10-dimensional Softmax probability vectors for test sets and custom single images.", tbl_cell_style),
            Paragraph("Executes inference mode forward-pass without backpropagation.", tbl_cell_style)
        ],
        [
            Paragraph("tf.keras.Model", tbl_cell_bold),
            Paragraph("<code>model_cnn.summary()</code>", tbl_cell_code),
            Paragraph("Printed layer names, output tensor shapes, and total trainable parameter count for the CNN.", tbl_cell_style),
            Paragraph("Essential for verifying tensor dimensionality and calculating network parameter complexity.", tbl_cell_style)
        ],
        [
            Paragraph("tensorflow.math", tbl_cell_bold),
            Paragraph("<code>confusion_matrix(labels, preds)</code>", tbl_cell_code),
            Paragraph("Computed a 10x10 contingency matrix comparing actual test labels against predicted labels.", tbl_cell_style),
            Paragraph("Pinpoints specific digit misclassifications (e.g. false positives between 4 and 9 or 3 and 5).", tbl_cell_style)
        ],
        # OpenCV Functions
        [
            Paragraph("cv2 (OpenCV)", tbl_cell_bold),
            Paragraph("<code>cv2.imread(path)</code>", tbl_cell_code),
            Paragraph("Loaded external custom images (e.g. <code>5.png</code> and user-prompted paths) into NumPy arrays.", tbl_cell_style),
            Paragraph("Standard high-performance computer vision image loader (loads in BGR format by default).", tbl_cell_style)
        ],
        [
            Paragraph("cv2 (OpenCV)", tbl_cell_bold),
            Paragraph("<code>cv2.cvtColor(src, code)</code>", tbl_cell_code),
            Paragraph("Converted BGR images to RGB (for Matplotlib display) and RGB to Grayscale (for model input).", tbl_cell_style),
            Paragraph("MNIST models expect single-channel grayscale inputs; OpenCV loads 3-channel color by default.", tbl_cell_style)
        ],
        [
            Paragraph("cv2 (OpenCV)", tbl_cell_bold),
            Paragraph("<code>cv2.resize(src, (28, 28))</code>", tbl_cell_code),
            Paragraph("Rescaled custom external images of arbitrary resolution down to exactly 28x28 pixels.", tbl_cell_style),
            Paragraph("Aligns spatial resolution with the exact input dimensions expected by the trained neural network.", tbl_cell_style)
        ],
        # NumPy Functions
        [
            Paragraph("numpy (np)", tbl_cell_bold),
            Paragraph("<code>np.unique(array)</code>", tbl_cell_code),
            Paragraph("Inspected target label arrays (<code>y_train</code>, <code>y_test</code>) to verify distinct classes [0..9].", tbl_cell_style),
            Paragraph("Confirms all 10 integer digits are present without unexpected class values.", tbl_cell_style)
        ],
        [
            Paragraph("numpy (np)", tbl_cell_bold),
            Paragraph("<code>np.argmax(a, axis)</code>", tbl_cell_code),
            Paragraph("Mapped 10-class probability vectors into single integer class predictions (0 through 9).", tbl_cell_style),
            Paragraph("Finds the index corresponding to maximum confidence output from Softmax.", tbl_cell_style)
        ],
        [
            Paragraph("numpy (np)", tbl_cell_bold),
            Paragraph("<code>np.reshape(a, [1, 28, 28])</code>", tbl_cell_code),
            Paragraph("Added a batch dimension of size 1 to single preprocessed test images before feeding into <code>predict()</code>.", tbl_cell_style),
            Paragraph("Keras inference expects batch-shaped tensors: (Batch_Size, Height, Width).", tbl_cell_style)
        ],
        [
            Paragraph("numpy (np)", tbl_cell_bold),
            Paragraph("<code>array / 255.0</code>", tbl_cell_code),
            Paragraph("Scaled pixel values from integer range [0, 255] down to floating point [0.0, 1.0].", tbl_cell_style),
            Paragraph("Min-Max normalization speeds up gradient descent convergence and prevents exploding gradients.", tbl_cell_style)
        ],
        # Matplotlib & Seaborn
        [
            Paragraph("matplotlib.pyplot", tbl_cell_bold),
            Paragraph("<code>plt.imshow(img)</code>", tbl_cell_code),
            Paragraph("Visualized digit images from MNIST and rendered preprocessed external input images.", tbl_cell_style),
            Paragraph("Renders 2D and 3D numeric arrays as graphical color or grayscale images.", tbl_cell_style)
        ],
        [
            Paragraph("matplotlib.pyplot", tbl_cell_bold),
            Paragraph("<code>plt.axis('off')</code>", tbl_cell_code),
            Paragraph("Removed coordinate axes, grid ticks, and borders when displaying input digit images.", tbl_cell_style),
            Paragraph("Creates clean visual presentations of image data without distracting coordinate scales.", tbl_cell_style)
        ],
        [
            Paragraph("matplotlib.pyplot", tbl_cell_bold),
            Paragraph("<code>plt.figure(figsize=(15,7))</code>", tbl_cell_code),
            Paragraph("Configured wide display dimensions for rendering the large 10x10 confusion matrix.", tbl_cell_style),
            Paragraph("Ensures matrix cell values and class tick labels remain legible without overlap.", tbl_cell_style)
        ],
        [
            Paragraph("seaborn (sns)", tbl_cell_bold),
            Paragraph("<code>sns.heatmap(data, annot, ...)</code>", tbl_cell_code),
            Paragraph("Plotted the 10x10 confusion matrix with integer counts (<code>fmt='d'</code>) and blue color intensity.", tbl_cell_style),
            Paragraph("Provides clear visual perception of classification density along the diagonal and off-diagonal errors.", tbl_cell_style)
        ],
        # Core Python
        [
            Paragraph("Python Built-in", tbl_cell_bold),
            Paragraph("<code>input('Prompt text')</code>", tbl_cell_code),
            Paragraph("Paused cell execution to prompt user for an image file path dynamically in the final cell.", tbl_cell_style),
            Paragraph("Enables interactive runtime prediction on arbitrary user-provided image files.", tbl_cell_style)
        ],
        [
            Paragraph("Python Built-in", tbl_cell_bold),
            Paragraph("<code>list.append() / int()</code>", tbl_cell_code),
            Paragraph("Collected argmax predictions across all 10,000 test cases into <code>y_pred_labels</code>.", tbl_cell_style),
            Paragraph("Constructs a clean integer list of predicted labels for confusion matrix consumption.", tbl_cell_style)
        ]
    ]

    func_table = Table(func_data, colWidths=[90, 115, 175, 160], repeatRows=1)
    func_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
    ]))
    story.append(func_table)
    story.append(Spacer(1, 14))

    # SECTION 3: Deep Technical Walkthrough by Phase
    story.append(Paragraph("3. Detailed Phase-by-Phase Technical Walkthrough", h1_style))

    # Phase 1 & 2
    story.append(Paragraph("Phase 1 & 2: Dataset Loading, Exploration & Normalization", h2_style))
    p1_text = (
        "The project begins by ingesting the MNIST benchmark via <code>datasets.mnist.load_data()</code>. "
        "The dataset contains 60,000 training images and 10,000 testing images of dimension 28x28 pixels. "
        "Exploration using <code>np.unique()</code> verifies that the target classes are balanced integers from 0 to 9. "
        "Because raw 8-bit image pixels range from 0 to 255, the notebook performs feature scaling: "
        "<br/><code>X_train = X_train / 255.0</code> and <code>X_test = X_test / 255.0</code>.<br/>"
        "<b>Why scaling is essential:</b> Unnormalized inputs with large numerical values cause severe gradient variance, "
        "slowing down backpropagation and potentially causing exploding gradients. Scaling to [0.0, 1.0] ensures stable, "
        "smooth optimization for the Adam optimizer."
    )
    story.append(Paragraph(p1_text, body_style))

    # Phase 3
    story.append(Paragraph("Phase 3: Baseline Neural Network (Dense ANN)", h2_style))
    p3_text = (
        "The first architecture built is a standard Multi-Layer Perceptron (ANN):"
        "<br/>• <b>Flatten Layer:</b> Unrolls the (28, 28) matrix into a 784-element feature vector."
        "<br/>• <b>Dense Hidden Layer 1:</b> 128 neurons with <code>ReLU</code> activation (introduces non-linear decision boundaries)."
        "<br/>• <b>Dense Hidden Layer 2:</b> 64 neurons with <code>ReLU</code> activation (extracts condensed hierarchical representations)."
        "<br/>• <b>Output Layer:</b> 10 neurons with <code>Softmax</code> activation (outputs probability distribution summing to 1.0)."
        "<br/>• <b>Loss & Optimizer:</b> <code>sparse_categorical_crossentropy</code> (avoids memory overhead of one-hot encoded vectors) "
        "paired with <code>Adam</code> (adaptive learning rates per parameter)."
        "<br/><b>Result:</b> Achieved <b>97.84% test accuracy</b> across 10 epochs."
    )
    story.append(Paragraph(p3_text, body_style))

    # Phase 4
    story.append(Paragraph("Phase 4: Diagnostics, Confusion Matrix & ANN Custom Image Test", h2_style))
    p4_text = (
        "To thoroughly evaluate the ANN, predictions on all 10,000 test images are obtained via <code>model.predict(X_test)</code>. "
        "Because Softmax outputs 10 probabilities per image, <code>np.argmax()</code> extracts the predicted class label. "
        "A 10x10 Confusion Matrix is generated using <code>tf.math.confusion_matrix()</code> and plotted via <code>sns.heatmap()</code>. "
        "This reveals that while overall accuracy is high, the ANN occasionally confuses visually similar digits (e.g. 4 vs 9, 3 vs 5, and 7 vs 2).<br/>"
        "When tested on an external custom image (<code>5.png</code>), the ANN predicted class <b>7</b> instead of 5. "
        "This highlights the core flaw of standard dense ANNs: flattening destroys 2D spatial locality and spatial invariance, making the model "
        "hypersensitive to minor line thickness, stroke positioning, and background contrast."
    )
    story.append(Paragraph(p4_text, body_style))

    # Phase 5
    story.append(Paragraph("Phase 5: Deep Convolutional Neural Network (CNN)", h2_style))
    p5_text = (
        "To resolve the limitations of the ANN, the project constructs a dedicated Convolutional Neural Network (CNN):"
        "<br/>• <b>Input Reshape:</b> Explicitly forms a <code>(28, 28, 1)</code> 3D tensor representing (Height, Width, Channel)."
        "<br/>• <b>Conv2D Block 1:</b> 32 filters of size (3x3) + ReLU. Learns local spatial filters such as horizontal/vertical edges and curves."
        "<br/>• <b>MaxPooling2D Block 1:</b> (2x2) pool window. Downsamples feature maps from 28x28 to 13x13, retaining the strongest feature activations."
        "<br/>• <b>Conv2D Block 2:</b> 64 filters of size (3x3) + ReLU. Synthesizes low-level features into complex digit components (loops, intersections)."
        "<br/>• <b>MaxPooling2D Block 2:</b> Downsamples feature maps from 13x13 to 5x5."
        "<br/>• <b>Flatten & Regularization:</b> Flattens 5x5x64 (1,600 values) followed by <code>Dropout(0.25)</code> to inhibit overfitting."
        "<br/>• <b>Dense Classification:</b> 64-neuron Dense layer + 10-neuron Softmax classification head."
        "<br/>• <b>Training & Performance:</b> Trained with batch size 64 and a 10% validation split. "
        "Achieved <b>99.21% test accuracy</b> on test data, decisively outperforming the ANN."
    )
    story.append(Paragraph(p5_text, body_style))

    # Phase 6
    story.append(Paragraph("Phase 6: Interactive Predictive System for Real-World Custom Images", h2_style))
    p6_text = (
        "The final section of the notebook creates an interactive inference system using OpenCV to classify user-supplied digit images:"
        "<br/>1. <b>Input Acquisition:</b> Prompts user for image path via <code>input()</code>."
        "<br/>2. <b>Image Reading:</b> <code>cv2.imread()</code> reads the image file."
        "<br/>3. <b>Display:</b> Converts BGR to RGB via <code>cv2.cvtColor()</code> and renders using <code>plt.imshow()</code>."
        "<br/>4. <b>Color Channel Conversion:</b> Converts RGB to single-channel Grayscale via <code>cv2.COLOR_RGB2GRAY</code>."
        "<br/>5. <b>Spatial Resizing:</b> <code>cv2.resize(grayscale, (28, 28))</code> rescales image to exact model dimensions."
        "<br/>6. <b>Normalization:</b> Divides pixel values by 255.0."
        "<br/>7. <b>Batch Dimension Injection:</b> <code>np.reshape(input_scaled, [1, 28, 28])</code> creates tensor shape <code>(1, 28, 28)</code>."
        "<br/>8. <b>Inference:</b> <code>model_cnn.predict()</code> outputs probabilities; <code>np.argmax()</code> prints the predicted digit."
    )
    story.append(Paragraph(p6_text, body_style))
    story.append(Spacer(1, 10))

    # SECTION 4: Key Insights & Recommendations
    story.append(Paragraph("4. Key Takeaways & Practical Recommendations", h1_style))

    takeaways = [
        ("Why CNN Outperformed ANN", "The baseline ANN achieved 97.84% by treating the 784 pixels independently, losing all spatial structure. The CNN achieved 99.21% because convolution filters preserve local 2D pixel neighborhoods, enabling translation-invariant stroke and curve detection."),
        ("Background Inversion Caution", "MNIST images feature white strokes on a solid black background (pixel values near 0 for background, near 255 for stroke). Real-world photos or scanned documents typically feature black ink on white paper. If an inverted image is fed into the system, OpenCV preprocessing should include <code>cv2.bitwise_not()</code> to invert colors before feeding to the model."),
        ("Aspect Ratio Preservation", "Directly calling <code>cv2.resize()</code> on non-square images can distort stroke aspect ratios. For production systems, it is recommended to pad rectangular images to a square aspect ratio before resizing to 28x28."),
        ("Model Persistence Recommendation", "Currently, the notebook trains models in memory. To avoid retraining across sessions, the trained CNN should be saved to disk using <code>model_cnn.save('mnist_cnn_model.keras')</code> and reloaded with <code>tf.keras.models.load_model()</code>.")
    ]

    for title, desc in takeaways:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 14))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_pdf()

