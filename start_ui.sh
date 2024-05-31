source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate sql_validation_rules
streamlit run ./sql_validation_rules/ui/streamlit_main.py --server.port=8086 --server.address=0.0.0.0
