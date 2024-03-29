from mutcov import testcase
from mutcov import mutant
import sys
import pytest
import io

from pathlib import Path
from contextlib import redirect_stdout
from typing import Dict
from typing import Iterable
from typing import List
from time import time
from _pytest.config.findpaths import get_dirs_from_args
from .testcase import Test
from coverage import CoverageData

DEFAULT_RUNNER = 'python -m pytest -x --assert=plain'

def main():
    
    test_paths: List[Path] = [Path('.').resolve()] #TODO add test dir
    if len(sys.argv) > 1:
        test_paths = get_dirs_from_args(sys.argv[1:])
    args = sys.argv[1:]
    output: List[str]
    with io.StringIO() as buf, redirect_stdout(buf):
        pytest.main(args=[args[0]] + ['--co', '-q'])
        output = buf.getvalue()
    str_list = output.split('\n')[ : -3]
    cov_mod = args[1] #TODO Path(args[0]).resolve().parts[-2]
    test_cov = {}
    for test in str_list:
        path_root_list = list(Path(args[0]).resolve().parts)[ : -2]
        # path_root_list.remove(path_root_list[-2])
        path_root = Path(path_root_list[0] + "/".join(path_root_list[1:]))
        test_path = str(path_root) + "/" + test
        with io.StringIO() as buf, redirect_stdout(buf):
            pytest.main(args=[test_path] + ['--cov=' + cov_mod, '-q', '--no-summary', '--no-header']) #TODO rework test path
        cov_data = CoverageData()
        cov_data.read()
        test_cov[test_path] = cov_data.lines('/home/pe4enko/Repos/flask/src/flask/templating.py')
    print(test_cov)

    import mutmut
    import mutmut.cache
    config = mutmut.Config(
        total=0,  # we'll fill this in later!
        swallow_output=False,
        test_command=DEFAULT_RUNNER,
        covered_lines_by_filename=None,
        coverage_data=None,
        baseline_time_elapsed=1.0,
        dict_synonyms='',
        using_testmon=False,
        tests_dirs=[str(path_root) + "/tests"],
        hash_of_tests='NO TESTS FOUND',
        test_time_multiplier=2.0,
        test_time_base=0.0,
        pre_mutation=None,
        post_mutation=None,
        paths_to_mutate='/home/pe4enko/Repos/flask/src/flask/templating.py',
        mutation_types_to_apply=set(mtype.strip() for mtype in ["expr_stmt"]), # set(mutmut.mutations_by_type.keys()),
        no_progress=False,
        rerun_all=False
    )
    from mutmut import Progress
    output_legend = {
        "killed": "🎉",
        "timeout": "⏰",
        "suspicious": "🤔",
        "survived": "🙁",
        "skipped": "🔇",
    }
    progress = Progress(total=config.total, output_legend=output_legend, no_progress=False)
    files = mutmut.python_source_files(path_root.joinpath("src"), 'tests')
    for file in files:
        if file == '/home/pe4enko/Repos/flask/src/flask/templating.py':
            mutations_by_file = {}
            mutmut.cache.update_line_numbers(file)
            mutmut.add_mutations_by_file(mutations_by_file, file, None, config)
    for mutated_file, mutants in mutations_by_file.items():
        for mutant in mutants:
            mutants_killed = progress.killed_mutants
            for test, lines in test_cov.items():
                if mutant.line_number + 1 in lines:
                    # print(mutant.line_number + 1, lines)
                    mut_by_file = {mutated_file: [mutant]}
                    config.test_command = "pytest -q --assert=plain " + test
                    with io.StringIO() as buf, redirect_stdout(buf):
                        mutmut.run_mutation_tests(config=config, progress=progress, mutations_by_file=mut_by_file)
                    progress.print()
                    if progress.killed_mutants > mutants_killed:
                        break
                    progress.surviving_mutants -= 1
            if progress.killed_mutants == mutants_killed:
                progress.surviving_mutants += 1
    # pytest.main(args=['--cov=/home/pe4enko/Repos/flask/src/flask', '/home/pe4enko/Repos/flask/tests/test_user_error_handler.py::TestGenericHandlers::test_handle_generic'])
    # pytest.main(args=[args[0]] + ['--cov=' + cov_mod])
    # print(sys.path)
    # tests: List[Test] = testcase.readTests(test_paths)
    # print(tests[0].name)

    # import pytest
    # from pytest import Session, Config, PytestPluginManager
    # from pytest_cov.plugin import CovPlugin
    # pluginmanager = PytestPluginManager()
    # pluginmanager.import_plugin('pytest_cov', True)
    # plugins = None
    # config = Config(
    #     pluginmanager,
    #     invocation_params=Config.InvocationParams(
    #         args=args or (),
    #         plugins=plugins,
    #         dir=Path.cwd(),
    #     ),
    # )
    # config.hook.pytest_load_initial_conftests(early_config=config, args=args)
    # pluginmanager.hook.pytest_configure(config=config)
    # plugin = CovPlugin(options, config.pluginmanager)
    # config.pluginmanager.register(plugin, '_cov')
    # collect = pytest.Node("initial")
    # session = Session.from_parent(collect)
    # session_test = session.perform_collect(args)
    
    #print(tests[0].name)
    # for test in tests:
    #     runCoverage(test)
    # mutants = createMutants()
    # for mutant in mutants:
    #     for test in tests:
    #         if mutant.location in test.coverage:
    #             mutant.add(test)
    # results = list[Result]
    # for mutant in mutants:
    #     results.append(mutant.execute())
    # printResults(results)

if __name__ == '__main__':
    main()
