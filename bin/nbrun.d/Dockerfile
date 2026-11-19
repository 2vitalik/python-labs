# bin/nbrun build → the image ods-nbrun, the box where students' notebooks run (T354). Building is the only step with network.
FROM python:3.12-slim
COPY requirements.txt /opt/nbrun/
RUN pip install --no-cache-dir -r /opt/nbrun/requirements.txt && useradd -u 1000 -M -d /tmp -s /usr/sbin/nologin nb
# The font cache once, here: a fresh one in every run would cost seconds (run_nb.py copies it into /tmp/mpl).
RUN MPLCONFIGDIR=/opt/mpl python -c "import matplotlib.pyplot as plt; plt.figure()" && chmod -R a+rX /opt/mpl
COPY run_nb.py engines.py /opt/nbrun/
# No index for pip: `!pip install x` of a missing package fails at once instead of retrying a network that is not there.
# One BLAS thread: the box has one CPU, and a dozen idle threads per process would eat the process limit.
ENV PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 \
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
USER 1000:1000
WORKDIR /tmp
ENTRYPOINT ["python", "/opt/nbrun/run_nb.py"]
