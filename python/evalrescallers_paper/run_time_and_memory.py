import json
import os
import subprocess
import textwrap


def json_to_tsv(json_dict, tsv_out):
    '''json_dict expected to be json object loaded from summary.json
    made by tb-amr-benchmarking pipeline'''
    with open(tsv_out, 'w') as f:
        print('Sample', 'Tool', 'RAM (MB)', 'Wall_clock (s)', sep='\t', file=f)

        for sample in sorted(json_dict):
            for tool, tool_dict in sorted(json_dict[sample].items()):
                if tool_dict['Success']:
                    ram_in_mb = round(tool_dict['time_and_memory']['ram'] / 1000, 2)
                    time_in_seconds = round(tool_dict['time_and_memory']['wall_clock_time'], 2)
                    print(sample, tool, ram_in_mb, time_in_seconds, sep='\t', file=f)


def tsv_to_plot(tsv_file, outprefix):
    '''Makes box plots of run time and memory,
    using TSV file made by json_to_tsv'''
    time_pdf = f'{outprefix}.time.pdf'
    memory_pdf = f'{outprefix}.memory.pdf'

    r_string = r'''        library(ggplot2)
        d = read.csv(file="''' + tsv_file + r'''", sep="\t", header=T)

        ggplot(d, aes(x=Tool, y=Wall_clock..s. / 60)) +
          geom_boxplot() +
          xlab("Tool") +
          ylab("Wall clock time (m)") +
        ggsave(filename="''' + time_pdf + '''", width=6, height=3, scale=0.85)


        ggplot(d, aes(Tool, RAM..MB.)) +
          geom_boxplot() +
          xlab("Tool") +
          ylab("Peak RAM (MB)") +
        ggsave(filename="''' + memory_pdf + '''", width=6, height=3, scale=0.85)

        file.remove("Rplots.pdf")'''

    r_script = f'{outprefix}.R'
    with open(r_script, 'w') as f:
        print(textwrap.dedent(r_string), file=f)
    subprocess.check_output(f'R CMD BATCH {r_script}', shell=True)
    os.unlink(f'{r_script}out')
    try:
        os.unlink('.RData')
    except:
        pass

