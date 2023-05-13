import vtk

from src.simple_pipeline import VisualisationPipeline

FILE_NAME = "../../data/vtks/grid_of_triangles.vtk"


def write_vtk(data: vtk.vtkUnstructuredGrid, filename: str):
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetInputData(data)
    writer.Write()


def read_vtk(filename: str) -> vtk.vtkUnstructuredGrid:
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()


def transform_grid(grid: vtk.vtkUnstructuredGrid, transform: vtk.vtkTransform):
    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(grid)
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    return transform_filter.GetOutput()


def print_dataset_info(dataset: vtk.vtkUnstructuredGrid):
    point_data = dataset.GetPointData()
    cell_data = dataset.GetCellData()

    print(f"Number of point data arrays: {point_data.GetNumberOfArrays()}")
    for j in range(point_data.GetNumberOfArrays()):
        array = point_data.GetArray(j)
        print(f"  Point data array {j}: {point_data.GetArrayName(j)}")
        print(f"    Number of components: {array.GetNumberOfComponents()}")
        print(f"    Number of tuples: {array.GetNumberOfTuples()}")
        print(f"    Range: {array.GetRange()}")

    print(f"Number of cell data arrays: {cell_data.GetNumberOfArrays()}")
    for j in range(cell_data.GetNumberOfArrays()):
        array = cell_data.GetArray(j)
        print(f"  Cell data array {j}: {cell_data.GetArrayName(j)}")
        print(f"    Number of components: {array.GetNumberOfComponents()}")
        print(f"    Number of tuples: {array.GetNumberOfTuples()}")
        print(f"    Range: {array.GetRange()}")


if __name__ == "__main__":

    # Read VTK file
    vtk_data = read_vtk(FILE_NAME)

    # Print dataset info
    print_dataset_info(vtk_data)

    # Display for verification
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(vtk_data)

    # Display
    pipeline = VisualisationPipeline(mappers=[mapper])
    pipeline.run()

    # Apply a translation transform
    transform = vtk.vtkTransform()
    transform.Scale(2.0, 1.0, 1.0)  # Double the size along the x-axis
    transform.RotateZ(45.0)  # Rotate 45 degrees about the z-axis
    vtk_data = transform_grid(vtk_data, transform)

    # Write VTK file
    write_vtk(vtk_data, "test.vtk")
