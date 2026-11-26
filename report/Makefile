PY ?= python3

all: main.pdf

main.pdf: main.tex sections/*.tex figures/*.png outputs/*.txt ../*.py
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	pdflatex -interaction=nonstopmode -halt-on-error main.tex

# re-run the scripts (from the repo root) to refresh program output and figures
outputs:
	cd .. && MPLBACKEND=Agg $(PY) problem1.py > report/outputs/problem1.txt
	cd .. && MPLBACKEND=Agg $(PY) problem2.py > report/outputs/problem2.txt
	cd .. && MPLBACKEND=Agg $(PY) problem3.py > report/outputs/problem3.txt
	cd .. && MPLBACKEND=Agg $(PY) problem4.py > report/outputs/problem4.txt
	cd .. && MPLBACKEND=Agg $(PY) problem5.py > report/outputs/problem5.txt
	cd .. && MPLBACKEND=Agg $(PY) problem6.py > report/outputs/problem6.txt

clean:
	rm -f main.aux main.log main.out main.pdf

.PHONY: all outputs clean
