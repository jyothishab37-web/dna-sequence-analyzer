from flask import Flask, render_template, request

app = Flask(__name__)
codon_table = {
    "AUG": "M",

    # Phenylalanine
    "UUU": "F",
    "UUC": "F",

    # Leucine
    "UUA": "L",
    "UUG": "L",

    # Alanine
    "GCU": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",

    # Stop codons
    "UAA": "Stop",
    "UAG": "Stop",
    "UGA": "Stop"
}
def validate_dna(seq):
    valid = set("ATGC")
    return all(base in valid for base in seq)

def transcribe_dna(seq):
    return seq.replace("T", "U")

def translate_rna(rna):
    protein = ""
    for i in range(0, len(rna), 3):
        codon = rna[i:i+3]
        if len(codon) < 3:
            break
        amino = codon_table.get(codon, "")
        if amino == "Stop":
            break
        protein += amino
    return protein

def gc_content(seq):
    g = seq.count("G")
    c = seq.count("C")
    return round(((g + c) / len(seq)) * 100, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    if request.method == "POST":
        dna = request.form["dna"].upper()

        if not validate_dna(dna):
            result["error"] = "Invalid DNA sequence!"
        else:
            rna = transcribe_dna(dna)
            protein = translate_rna(rna)
            gc = gc_content(dna)

            result = {
                "dna": dna,
                "rna": rna,
                "protein": protein,
                "gc": gc
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)