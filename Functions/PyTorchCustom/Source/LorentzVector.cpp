#include <torch/extension.h>
#include <iostream>

torch::Tensor ToPxPyPzE(float pt, float eta, float phi, float e, std::string device)
{
  torch::TensorOptions options = torch::TensorOptions().dtype(torch::kFloat32); 
  if (device == "cuda"){ options = options.device(torch::kCUDA); }

  return torch::tensor({
      pt*std::cos(phi), 
      pt*std::sin(phi), 
      pt*std::sinh(eta), 
      e}, options);
}

torch::Tensor GetMass(torch::Tensor v)
{

  torch::Tensor val = v[3]*v[3] - v[0]*v[0] - v[1]*v[1] - v[2]*v[2]; 
  val.index_put_({val < 0}, -at::sqrt(abs(val))/1000);
  val.index_put_({val >= 0}, at::sqrt(val)/1000);
  return val; 
}



PYBIND11_MODULE(TORCH_EXTENSION_NAME, m)
{
  m.def("ToPxPyPzE", &ToPxPyPzE, "Convert Rapidity to Cartesian"); 
  m.def("GetMass", &GetMass, "Calculate Invariant Mass");
}