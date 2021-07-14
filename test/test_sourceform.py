from ford.sourceform import FortranSourceFile

from collections import defaultdict


def test_extends(tmp_path):
    """Check that types can be extended"""

    data = """\
    program foo
    !! base type
    type :: base
    end type base

    !! derived type
    type, extends(base) :: derived
    end type

    !! derived type but capitalised
    type, EXTENDS(base) :: derived_capital
    end type

    end program foo
    """

    filename = tmp_path / "test.f90"
    with open(filename, "w") as f:
        f.write(data)

    settings = defaultdict(str)
    settings["docmark"] = "!"

    fortran_type = FortranSourceFile(str(filename), settings)

    assert len(fortran_type.programs) == 1

    program = fortran_type.programs[0]

    assert len(program.types) == 3
    assert program.types[1].extends == "base"
    assert program.types[2].extends == "base"


def test_submodule_procedure_contains(tmp_path):
    """Check that submodule procedures can have 'contains' statements"""

    data = """\
    module foo_m
      implicit none
      interface
        module subroutine foo()
          implicit none
        end subroutine
      end interface
    end module

    submodule(foo_m) foo_s
      implicit none
    contains
      module procedure foo
      contains
        subroutine bar()
        end subroutine
      end procedure
    end submodule
    """

    filename = tmp_path / "test.f90"
    with open(filename, "w") as f:
        f.write(data)

    settings = defaultdict(str)
    settings["docmark"] = "!"

    fortran_type = FortranSourceFile(str(filename), settings)

    assert len(fortran_type.modules) == 1
