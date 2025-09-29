import type { UseFormRegisterReturn } from "react-hook-form"

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  register?: UseFormRegisterReturn
  label?: string
}

export const TextInput = ({ id, placeholder, name, label, register, disabled, ...props }: InputProps) => {
  return (
    <>
      {label && <label htmlFor={id} className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">{label}</label>}
      <input
        className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
        {...props}
        disabled={disabled}
        type="text"
        name={name}
        id={id}
        placeholder={placeholder}
      />
    </>
  )

}

export const NumberInput = () => {

}

export const CheckBox = () => {

}
