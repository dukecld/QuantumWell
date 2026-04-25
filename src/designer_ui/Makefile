# Makefile for quantumWell.py and associaed ui files created in QDesigner.
#    Charlie Duke
#    Grinnell College
#    January 2019.

#  makes use of make's automatic variables to facilitate future changes in pyuic
#  conversion code.

# dependency:  make facility. included in Linus distributions and in osx XCode.
# usage:  execute make command from command line in Linux and osX. All out of date
#            .ui files converted to .py files prior to opening quantumWell.py

#          for Windows: execute run_pyuic_Windows.bat file in src directory

PYTHON=python
PYUIC=pyuic5
SW=-x
OW=-o


openGui: ../ui/ui_AddBarrierDock.py ../ui/ui_AddSHODock.py \
../ui/ui_AddSlopedPotentialDock.py ../ui/ui_BuildWellDock.py \
../ui/ui_FindStatesWellDock.py ../ui/ui_MainDockWidget.py \
../ui/ui_MessageDock.py ../ui/ui_RemoveBarrierDock.py \
../ui/ui_SolveWellDock.py ../ui/ui_AddMultiBarriersDock.py \
../ui/ui_InfoDock.py ../ui/ui_AddVpeDock.py

../ui/ui_AddBarrierDock.py: AddBarrierDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_AddSHODock.py: AddSHODock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_AddSlopedPotentialDock.py: AddSlopedPotentialDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_BuildWellDock.py: BuildWellDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_AddMultiBarriersDock.py: AddMultiBarriersDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_FindStatesWellDock.py: FindStatesWellDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_MainDockWidget.py: MainDockWidget.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_MessageDock.py: MessageDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_RemoveBarrierDock.py: RemoveBarrierDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_SolveWellDock.py: SolveWellDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_InfoDock.py: InfoDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@

../ui/ui_AddVpeDock.py: AddVpeDock.ui
	$(PYUIC) $(SW) $^ $(OW) $@
