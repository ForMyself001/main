
using System.Windows.Forms;

class Program
{
    static void Main()
    {
        // пути к файлам
        string inFile = "in.txt";
        string oFile = "out.txt";

        Dictionary<string, List<int>> midResult = new Dictionary<string, List<int>>();
        List<string> result = new List<string> { "Коды\tДолжность" };

        try
        {
            if (File.Exists(inFile))
            {
                // Чтение исходного файла 
                foreach (var line in File.ReadLines(inFile).Skip(1))
                {
                    // разделение
                    var col = line.Split('\t');
                    //string name = col[0];
                    int code = int.Parse(col[1]);
                    string profession = col[2];

                    // формирование коллекции
                    if (!midResult.ContainsKey(profession))
                    {
                        midResult[profession] = new List<int>();
                    }
                    midResult[profession].Add(code);
                }
            }
        }
        catch (IOException ex)
        {
            Console.WriteLine($"Ошибка при работе с файлом: {ex.Message}");
        }


        // Формирование результата
        foreach (KeyValuePair<string, List<int>> kvp in midResult)
        {
            string prof = kvp.Key;
            List<int> codes = kvp.Value;
            // Преобразуем список кодов в строку с диапазонами
            string format = Format(codes);
            result.Add($"{format}\t{prof}");
        }

        // Запись результата в файл
        File.WriteAllLines(oFile, result);
    }

    // список кодов в диапазоны 
    static string Format(List<int> codes)
    {
        List<string> ranges = new List<string>();

        codes.Sort();

        int first = codes[0];
        int second = codes[0];

        for (int i = 1; i < codes.Count; i++)
        {
            if (codes[i] == second + 1)
            {
                second = codes[i];
            }
            else
            {
                AddRange(ranges, first, second);

                first = codes[i];
                second = codes[i];
            }
        }
        AddRange(ranges, first, second);

        void AddRange(List<string> ranges, int first, int second)
        {
            if (first == second)
            {
                ranges.Add(first.ToString());
            }
            else if (first +1  == second)
            {
                ranges.Add($"{first}, {second}");
            }
            else
            {
                ranges.Add($"{first}-{second}");
            }
        }

        return string.Join(", ", ranges);
    }
}