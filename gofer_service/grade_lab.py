import subprocess
import argparse
import os
import json
import asyncio
import async_timeout


async def grade_lab(submission, section='3', lab='lab01'):
    lab_container_path_template = '/srv/repo/materials/x18/lab/{section}/{lab}/{lab}.ipynb'
    grader_image = 'gofer'
    command = [
            'docker', 'run',
            '--rm',
            '-m', '2G',
            '-i',
            '--net=none',
            grader_image,
            "/srv/repo/grading/containergrade.bash",
            lab_container_path_template.format(section=section, lab=lab)
        ]
    process = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    with open(submission) as f:
        content = f.read().encode('utf-8')
        try:
            async with async_timeout.timeout(300):
                stdout, stderr = await process.communicate(content)
        except asyncio.TimeoutError:
            print(f'Grading timed out for {submission}')
            return False
        for line in stderr.decode('utf-8').split('\n'):
            if line.strip() == '':
                # Ignore empty lines
                continue
            if 'Killed' in line:
                # Our container was killed, so let's just skip this one
                return False
            if not line.startswith('WARNING:'):
                print(line)
                raise Exception("Found unrecognized output in stderr from {}, halting".format(' '.join(command)))
    lines = stdout.decode("utf-8").strip().split("\n")
    # print(lines)
    grade = float(lines[-1])
    # print(grade)

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(grade_lab())
    loop.run_until_complete(task)

